import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from contextlib import redirect_stdout
from interpreter.bodhi import translate

HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>BodhiScript</title>
<style>
body{margin:0;background:#000;color:#fff;font:14px monospace}
main{max-width:800px;margin:30px auto;padding:15px}
textarea,.out{box-sizing:border-box;width:100%;background:#000;color:#fff;border:1px solid #333;padding:12px;font:14px monospace}
textarea{height:220px;resize:vertical}
.out{margin-top:10px;min-height:60px;white-space:pre-wrap}
h1{font-size:20px}
p{color:#aaa}
code{color:#fff}
</style>
</head>
<body>
<main>
<h1>bodhiScript Demo</h1>
<p>Press <code>Ctrl/Cmd + Enter</code> to run.</p>
<p><b>Instructions</b></p>
<p>
<code>likha()</code> prints text.<br>
<code>maan</code> creates a variable.<br>
<code>yadi</code> creates a condition.<br>
Use <code>{ }</code> to group code.
</p>
<textarea id="code" spellcheck="false">likha("Hello from BodhiScript!");</textarea>
<div class="out" id="out"></div>
</main>

<script>
const code=document.querySelector('#code');
const out=document.querySelector('#out');

function run(){
  fetch('/run',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({code:code.value})
  }).then(r=>r.json()).then(x=>out.textContent=x.output||'');
}

code.addEventListener('keydown',e=>{
  const s=code.selectionStart;
  const end=code.selectionEnd;
  const v=code.value;

  if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){
    e.preventDefault();
    run();
    return;
  }

  if(e.key==='Tab'){
    e.preventDefault();
    code.setRangeText('    ',s,end,'end');
    return;
  }

  if(e.key==='Enter'){
    e.preventDefault();

    const before=v.slice(0,s);
    const line=before.split('\\n').pop();
    const indent=line.match(/^\\s*/)[0];

    const pairs={'(':')','[':']','{':'}'};
    const previous=v[s-1];
    const next=v[s];

    if(pairs[previous]===next){
      const inner=indent+'    ';
      code.setRangeText('\\n'+inner+'\\n'+indent,s,end,'end');
      code.selectionStart=code.selectionEnd=s+1+inner.length;
      return;
    }

    const extra=/[({[]\\s*$/.test(line.trim())?'    ':'';
    code.setRangeText('\\n'+indent+extra,s,end,'end');
    code.selectionStart=code.selectionEnd=s+1+indent.length+extra.length;
    return;
  }

  const pairs={'(':')','[':']','{':'}','"':'"'};

  if(pairs[e.key]&&s===end){
    const close=pairs[e.key];

    if(v[s]===close){
      e.preventDefault();
      code.selectionStart=code.selectionEnd=s+1;
      return;
    }

    e.preventDefault();
    code.setRangeText(e.key+close,s,s,'end');
    code.selectionStart=code.selectionEnd=s+1;
    return;
  }

  if([')',']','}'].includes(e.key)&&s===end&&v[s]===e.key){
    e.preventDefault();
    code.selectionStart=code.selectionEnd=s+1;
  }
});
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_error(404)
            return

        body=HTML.encode()
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Content-Length',len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != '/run':
            self.send_error(404)
            return

        length=int(self.headers.get('Content-Length',0))
        data=json.loads(self.rfile.read(length))
        out=io.StringIO()

        try:
            with redirect_stdout(out):
                exec(translate(data.get('code','')))
            result={'output':out.getvalue(),'status':'ok'}
        except Exception as e:
            result={'output':f'{type(e).__name__}: {e}','status':'error'}

        body=json.dumps(result).encode()
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self,*args):
        pass

if __name__=='__main__':
    for port in (8000,8001,8002,8080):
        try:
            server=ThreadingHTTPServer(('0.0.0.0',port),Handler)
            print(f'Open http://localhost:{port}')
            server.serve_forever()
            break
        except OSError:
            continue