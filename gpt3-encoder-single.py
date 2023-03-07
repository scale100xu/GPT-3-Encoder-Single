# -*- coding: utf-8 -*-
import os
import json,base64

project_dir = "./"
with open(os.path.join(project_dir, "encoder.json"), "r") as f:
    encoder = json.load(f)
with open(os.path.join(project_dir, "vocab.bpe"), "rb") as f:
    bpe_data = f.read()

with open(os.path.join(project_dir,"Encoder.js"), "r", encoding='utf-8',) as f:
    encoder_js = f.read()

encoder_js = encoder_js.split("\n")

encoder = "const encoder="+json.dumps(encoder)+";"
def bytes_to_unicode():

    bs = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    cs = bs[:]
    n = 0
    for b in range(2 ** 8):
        if b not in bs:
            bs.append(b)
            cs.append(2 ** 8 + n)
            n += 1
    cs = [chr(n) for n in cs]
    return dict(zip(bs, cs))

byte_encoder = bytes_to_unicode()
bpe_file_lines = ""

bpe_file_base64 = str(base64.b64encode(bpe_data))
bpe_file = "bpe_file='"+bpe_file_base64[2:len(bpe_file_base64)-1]+"';"
bpe_file += """
function base64Decode(base64) {
  const binaryString = window.atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes;
}
    bytes = base64Decode(bpe_file);
    const decoder_bpe = new TextDecoder('utf8');
    bpe_file = decoder_bpe.decode(bytes);
"""

encoder_js_file = ""

encoder_js_file += encoder+"\n"
encoder_js_file += bpe_file+"\n"
for i, encoder_one in enumerate(encoder_js):
    # filter 0~6 line
    if i<=6:
        continue
    # filter >= 174 line
    if i>=174:
        continue
    encoder_js_file += encoder_one + "\n"


with open(os.path.join(project_dir, "gpt3-encoder-single.js"), 'w', encoding='utf-8') as f:
    f.write(encoder_js_file)

