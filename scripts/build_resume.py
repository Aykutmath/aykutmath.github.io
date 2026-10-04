# Requires reportlab and pypdf. Run: python3 scripts/build_resume.py
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parents[1])
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from xml.sax.saxutils import escape
import re
from pypdf import PdfReader
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='NameCustom',fontName='Helvetica-Bold',fontSize=22,leading=26,textColor=HexColor('#245b75'),spaceAfter=8))
styles.add(ParagraphStyle(name='BodyCustom',fontName='Helvetica',fontSize=9.5,leading=13,spaceAfter=5))
styles.add(ParagraphStyle(name='SectionCustom',fontName='Helvetica-Bold',fontSize=12,leading=16,textColor=HexColor('#245b75'),spaceBefore=12,spaceAfter=6))
styles.add(ParagraphStyle(name='RoleCustom',fontName='Helvetica-Bold',fontSize=10,leading=14,spaceBefore=8,spaceAfter=4,keepWithNext=True))
def clean(t):return t.replace('—','-').replace('’',"'").replace('·',' | ')
def text(t,style='BodyCustom'):
 return Paragraph(escape(clean(t)),styles[style])
flow=[text('Aykut Arslan, PhD','NameCustom'),text('AI Research Engineer | Foundation Models, Agents, Post-Training, and Evaluation','RoleCustom'),Paragraph('Bellevue, WA | <link href="mailto:aykutmath@gmail.com">aykutmath@gmail.com</link><br/><link href="https://aykutmath.github.io">aykutmath.github.io</link> | <link href="https://www.linkedin.com/in/aykut-arslan-math">LinkedIn</link>',styles['BodyCustom']),text('PROFILE','SectionCustom'),text('AI research engineer and applied mathematician working across foundation-model training, post-training, autonomous agents, frontier-model evaluation, and formal reasoning. I build reproducible experimental systems for long-horizon agent evaluation, training-data quality, automated verification, and rigorous failure analysis.'),text('EXPERIENCE','SectionCustom')]
for line in Path('_includes/professional-experience.md').read_text().splitlines():
 if line.startswith('### '):flow.append(text(line[4:],'RoleCustom'))
 elif line.startswith('**'):flow.append(text(line.replace('**','')))
 elif line.startswith('- '):flow.append(Paragraph('&#8226; '+escape(clean(line[2:])),styles['BodyCustom']))
flow.extend([PageBreak(),text('RESEARCH & ENGINEERING','SectionCustom')])
for line in Path('_includes/selected-projects.md').read_text().splitlines():
 if line.startswith('### '):flow.append(text(line[4:],'RoleCustom'))
 elif line and not line.startswith(('#','<')):flow.append(text(line.replace('**','')))
flow.append(text('SELECTED PUBLICATIONS','SectionCustom'))
for title,detail,url in [('The Strict Threshold for Gaussian Ellipsoid Fitting','A. Arslan. Meta AI Research, 2026.','https://ai.meta.com/research/publications/the-strict-threshold-for-gaussian-ellipsoid-fitting/'),('Tightness of the Cycle-Based Relaxation for Completed Length-Three Alpha-Cycles','A. Arslan. Meta AI Research, 2026. Complete, machine-checked Lean formalization.','https://ai.meta.com/research/publications/tightness-of-the-cycle-based-relaxation-for-completed-length-three-alpha-cycles/'),('Adaptive Decision Policies for Long-Horizon Research Agents with Recursive Policy Improvement','A. Arslan. Submitted to ICLR 2027.',None)]:
 flow.append(Paragraph('<link href="'+url+'">'+escape(title)+'</link>' if url else escape(title),styles['RoleCustom']));flow.append(text(detail))
flow.extend([text('TECHNICAL SKILLS','SectionCustom'),text('Python, PyTorch, Lean, SQL, Linux, Docker, Git, AWS Bedrock, LLM APIs, distributed PyTorch training, mixed precision, checkpointing, sandboxed execution, trace replay, automated verification, agent evaluation, LLM-as-a-judge, experimental design, high-dimensional statistics, optimization, formal verification.'),text('EDUCATION','SectionCustom'),text('University of Southern California - Ph.D., Applied Mathematics (Statistics Concentration), 2017-2023; M.S., Statistics, 2021-2023.'),text('Middle East Technical University - B.S., Mathematics.')])
Path('files').mkdir(exist_ok=True)
out='files/Aykut_Arslan_Resume.pdf'
def footer(c,d):
 c.setFont('Helvetica',8);c.setFillColor(HexColor('#657581'));c.drawString(40,25,'Aykut Arslan, PhD');c.drawRightString(572,25,str(d.page))
SimpleDocTemplate(out,pagesize=(612,792),rightMargin=40,leftMargin=40,topMargin=35,bottomMargin=40,title='Aykut Arslan, PhD - Resume',author='Aykut Arslan').build(flow,onFirstPage=footer,onLaterPages=footer)
print('Resume pages:',len(PdfReader(out).pages))
