# coding=utf-8

from distutils.core import setup 
import py2exe 
 
setup(name="LineDetection", 
 version="1.0", 
 description="Sistema de detección de lineas", 
 author="Antonio de los Mozos Alonso", 
 author_email="ama0114@alu.ubu.es", 
 url="https://github.com/ama0114/TFG-OpenCV", 
 license="MIT", 
 scripts=["ejecucion.py"], 
 console=["ejecucion.py"], 
 options={"py2exe": {"bundle_files": 1}}, 
 zipfile=None,
)