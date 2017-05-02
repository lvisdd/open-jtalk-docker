#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import subprocess
import tempfile
import urllib.parse

from flask import Flask
from flask import Response, render_template, request

app = Flask(__name__)

# @app.route('/')
# def hello():
#     return 'Hello world!'
# 
# @app.route("/wav")
# def streamwav():
#     def generate():
#         with open("./static/wav/test.wav", "rb") as fwav:
#             data = fwav.read(1024)
#             while data:
#                 yield data
#                 data = fwav.read(1024)
#     return Response(generate(), mimetype="audio/x-wav")

@app.route('/')
def home():
  return render_template('index.html')

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.route("/speak", methods=['GET', 'POST'], strict_slashes=False)
def streamwav():
  def generate(text="テキストを入力してください。", emotion='normal', s=44000, p=128, a=0.5, b=0.0, r=1.0, fm=0.0, u=0.5, jm=1.0, jf=1.0, g=0.0, z=0):
    with tempfile.TemporaryDirectory() as tmpdirname:
      open_jtalk = ['open_jtalk']
      mech = ['-x','/usr/local/lib/open_jtalk_dic_utf_8-1.09']
      htsvoice = ['-m','/usr/local/src/mei/mei_' + emotion + '.htsvoice']
      cmd = open_jtalk + mech + htsvoice
      if not s is None:
        sampling_frequency = ['-s ', str(s) ]
        cmd = cmd + sampling_frequency
      
      if not p is None:
        frame_period       = ['-p ', str(p) ]
        cmd = cmd + frame_period
      
      if not a is None:
        all_pass_constant  = ['-a ', str(a) ]
        cmd = cmd + all_pass_constant
      
      postfiltering_coefficient = ['-b ' , str(b) ]
      speech_speed_rate         = ['-r ' , str(r) ]
      additional_half_tone      = ['-fm ', str(fm)]
      voiced_unvoiced_threshold = ['-u ' , str(u) ]
      weight_of_gv_for_spectrum = ['-jm ', str(jm)]
      weight_of_gv_for_log_f0   = ['-jf ', str(jf)]
      volume                    = ['-g ' , str(g) ]
      audio_buffer_size         = ['-z ' , str(z) ]
      outwav = ['-ow',tmpdirname + '/open_jtalk.wav']
      
      cmd = cmd + \
            postfiltering_coefficient + \
            speech_speed_rate + \
            additional_half_tone + \
            voiced_unvoiced_threshold + \
            weight_of_gv_for_spectrum + \
            weight_of_gv_for_log_f0 + \
            volume + \
            audio_buffer_size + \
            outwav
      print(cmd)
      c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
      c.stdin.write(text.encode('utf-8'))
      c.stdin.close()
      c.wait()
      with open(tmpdirname + '/open_jtalk.wav', "rb") as fwav:
        data = fwav.read(1024)
        while data:
          yield data
          data = fwav.read(1024)
  
  try:
    if request.method == 'POST':
        text    = request.form['text']
        emotion = request.form['emotion']
        s       = request.form['s']
        p       = request.form['p']
        a       = request.form['a']
        b       = request.form['b']
        r       = request.form['r']
        fm      = request.form['fm']
        u       = request.form['u']
        jm      = request.form['jm']
        jf      = request.form['jf']
        g       = request.form['g']
        z       = request.form['z']
    else:
        text    = request.args.get('text', default="テキストを入力してください。", type=str)
        emotion = request.args.get('emotion', default="normal", type=str)
        s       = request.args.get('s',  default=44000, type=int)
        p       = request.args.get('p',  default=128,   type=int)
        a       = request.args.get('a',  default=0.5,   type=int)
        b       = request.args.get('b',  default=0.0,   type=float)
        r       = request.args.get('r',  default=1.0,   type=float)
        fm      = request.args.get('fm', default=0.0,   type=float)
        u       = request.args.get('u',  default=0.5,   type=float)
        jm      = request.args.get('jm', default=1.0,   type=float)
        jf      = request.args.get('jf', default=1.0,   type=float)
        g       = request.args.get('g',  default=0.0,   type=float)
        z       = request.args.get('z',  default=0,     type=int)
  except:
        pass
  return Response(generate(text, emotion, s, p, a, b, r, fm, u, jm, jf, g, z), mimetype="audio/x-wav")

if __name__ == '__main__':
  app.run(host='0.0.0.0')
