"""Minimal 'brotli' shim for fontTools WOFF2 output, backed by Node's built-in zlib brotli.
Used only because the Python brotli wheel is unavailable offline in this environment."""
import subprocess
MODE_GENERIC, MODE_TEXT, MODE_FONT = 0, 1, 2
_JS_C = ("const z=require('zlib');const c=[];process.stdin.on('data',d=>c.push(d)).on('end',()=>{"
         "const o=z.brotliCompressSync(Buffer.concat(c),{params:{[z.constants.BROTLI_PARAM_MODE]:%d,"
         "[z.constants.BROTLI_PARAM_QUALITY]:11,[z.constants.BROTLI_PARAM_LGWIN]:22}});process.stdout.write(o)})")
_JS_D = ("const z=require('zlib');const c=[];process.stdin.on('data',d=>c.push(d)).on('end',()=>{"
         "process.stdout.write(z.brotliDecompressSync(Buffer.concat(c)))})")
def compress(data, mode=MODE_GENERIC, quality=11, lgwin=22, lgblock=0):
    return subprocess.run(["node","-e",_JS_C % mode], input=bytes(data), capture_output=True, check=True).stdout
def decompress(data):
    return subprocess.run(["node","-e",_JS_D], input=bytes(data), capture_output=True, check=True).stdout
