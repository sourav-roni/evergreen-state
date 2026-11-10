"""Extract original guide illustrations; preserve existing IDs and learning history."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,base64,subprocess
root=Path(__file__).resolve().parent.parent
app=root/'Evergreen-Drive'; f=app/'content.js'
c=json.loads(f.read_text().removeprefix('window.CONTENT = ').rstrip(';\n'))
visuals={}
(root/'research').mkdir(exist_ok=True)
subprocess.run(['pdftoppm','-f','132','-l','133','-scale-to','2500','-png',str(app/'assets/washington-driver-guide.pdf'),str(root/'research/markings')],check=True)
for page in [114,119,120]:
 subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','2500','-png','-singlefile',str(app/'assets/washington-driver-guide.pdf'),str(root/f'research/hi-page-{page}')],check=True)
def crop(key,page,box,alt,kind='sign',source=None):
 im=Image.open(source or root/f'research/hi-page-{page}.png').convert('RGB').crop(tuple(v*2 for v in box))
 import io
 b=io.BytesIO(); im.save(b,format='PNG',optimize=True)
 visuals[key]={'src':'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode(),'page':page,'alt':alt,'kind':kind,'crop':list(box)}
 return im
rows=[
(119,(110,530,220,638),'Cross road','A black cross on a yellow diamond.','A side road joins from the right','A divided highway begins','A railroad crossing'),
(119,(335,530,445,638),'Curve','A thick black arrow curves left on a yellow diamond.','A sharp right turn','Reversing curves','A winding road'),
(119,(560,530,670,638),'Deer crossing','A leaping deer silhouette on a yellow diamond.','A pedestrian crossing','A school crossing','A farm vehicle crossing'),
(119,(110,677,220,780),'Hill','A truck descending a slope on a yellow diamond.','A low bridge','A truck-only lane','A loading zone'),
(119,(335,677,445,780),'Low clearance','Vertical opposing arrows surround a height of 14 feet 4 inches.','A minimum following distance','A recommended speed','A lane width'),
(119,(560,677,670,780),'Merge','A yellow diamond shows the right roadway edge narrowing toward a dashed lane line.','An added lane with no merge required','A divided highway begins','Two-way traffic'),
(119,(110,820,220,925),'Merging traffic','A yellow diamond shows a straight arrow with a diagonal branch joining it.','A side road with no merge','A no-passing zone','An added lane with no merge required'),
(119,(338,820,464,925),'No passing zone','A yellow right-pointing pennant reads NO PASSING ZONE.','A passing lane begins','A school zone ends','A required left turn'),
(119,(560,820,670,925),'Pedestrian crossing','A walking person appears on a yellow diamond.','A school crossing','A bicycle crossing','A recreation trail'),
(119,(110,965,220,1070),'Reversing curves','A black arrow bends one way then the other on a yellow diamond.','A single sharp turn','A roundabout','An added lane'),
(119,(335,965,445,1070),'School crossing','Two walking figures appear on a yellow pentagon-shaped sign.','A recreation area','A pedestrian-only street','A school parking area'),
(119,(560,965,670,1070),'Side road','A yellow diamond shows a vertical bar with a short branch on its right.','A cross road','A divided highway ends','A merge from the left'),
(120,(110,8,220,142),'Signal ahead','A red-yellow-green traffic light symbol on a yellow diamond.','A stop sign ahead','A railroad crossing','A lane closure'),
(120,(335,8,445,142),'Slippery when wet','A car with curving tire tracks appears on a yellow diamond.','A winding road','A steep hill','A divided highway ends'),
(120,(560,8,670,142),'Soft shoulder','A yellow diamond reads SOFT SHOULDER.','A paved passing lane','A required stopping place','A road closure'),
(120,(110,187,220,290),'Stop ahead','An upward black arrow appears above a red octagon on a yellow diamond.','A yield ahead','A signal ahead','A no-entry road'),
(120,(335,187,445,290),'Sharp turn','A black arrow bends sharply left on a yellow diamond.','A gradual curve','A winding road','A roundabout'),
(120,(560,187,670,290),'Two-way traffic','Two black vertical arrows point in opposite directions on a yellow diamond.','A one-way road','A divided highway begins','An added lane'),
(120,(110,333,220,431),'Added lane; no merging required','A yellow diamond shows parallel forward lanes; the right lane curves in and continues beside the left.','Merging traffic that must join one lane','A lane ends immediately','A divided highway ends'),
(120,(335,333,445,431),'Advance warning of bicyclists','A bicycle symbol appears on a yellow diamond.','Motorcycles only','A bicycle repair shop','No bicycles allowed'),
(120,(560,333,670,431),'Narrow road or bridge ahead','A yellow diamond shows both road edges narrowing inward.','A divided highway begins','A lane added on the right','A mandatory stop'),
(120,(110,523,220,630),'Circular intersection','Three curved black arrows form a circle on a yellow diamond.','A U-turn prohibition','A winding road','A reverse-direction lane'),
(120,(335,523,445,662),'Left curve; 35 mph recommended','A left-curving arrow is above a yellow 35 MPH plaque.','A mandatory minimum of 35 mph','A right curve at 35 mph','A 35-mile distance to the next exit'),
(120,(560,523,670,630),'Divided highway begins','A yellow diamond shows opposing arrows curving around a divider at the top.','A divided highway ends','Two lanes merge into one','A no-passing zone')]
thumbs=[]
for i,(page,box,answer,alt,*wrong) in enumerate(rows):
 key=f'sign-{i+1:02}'; thumbs.append(crop(key,page,box,alt))
 q={'id':f'v{i+1:03}','module':'signals','page':page,'section':'4.12','prompt':'What does the sign shown mean?','choices':[answer,*wrong],'answer':0,'explanation':f'The official guide identifies this sign as: {answer.lower()}. Recognize the symbol and shape as well as its color.','visual':key,'visualQuestion':True}
 if not any(x['id']==q['id'] for x in c['questions']): c['questions'].append(q)
# Diagram crops exclude explanatory text. Reuse existing question IDs.
for key,box,alt in [('white-dashed',(86,84,364,176),'Two same-direction lanes separated by a dashed white line.'),('white-double',(86,412,364,501),'Two same-direction lanes separated by two solid white lines.'),('yellow-double',(82,969,367,1057),'Opposing traffic separated by two solid yellow centerlines.')]:
 crop(key,132,box,alt,'diagram',root/'research/markings-132.png')
crop('center-turn',133,(78,648,360,1042),'A center lane with left-turn arrows in opposite directions, between opposing through lanes.','diagram',root/'research/markings-133.png')
for q in c['questions']:
 if q['module']=='lanes':
  if 'dashed white lane line' in q['prompt']:q['visual']='white-dashed';q['visualQuestion']=True
  if 'double solid white' in q['prompt']:q['visual']='white-double';q['visualQuestion']=True
  if 'shared center turn lane' in q['prompt']:q['visual']='center-turn'
# Existing road signs: embed the guide's sign rather than a synthetic drawing.
crop('stop',114,(106,119,231,254),'A red octagonal sign with the word STOP.')
for q in c['questions']:
 if 'STOP sign' in q['prompt']:q['visual']='stop'
# Six new visual marking scenarios support all 20 mock forms.
markings=[('white-dashed','When is it permitted to cross the line shown?','When changing lanes safely',['Never under any circumstances','Only to drive against traffic','Whenever another driver honks'],'A dashed white line separates same-direction lanes. You may cross it to change lanes when safe.'),('white-double','May you cross the two solid white lines shown?','No; crossing double solid white lines is illegal',['Yes, whenever the other lane is empty','Yes, if you signal first','Yes, to pass slow traffic'],'The guide treats double solid white lines as a barrier between lanes.'),('yellow-double','May you cross these centerlines to pass another vehicle?','No, passing is prohibited in both directions',['Yes, when the opposite lane is empty','Yes, after sounding the horn','Yes, only in daylight'],'Double solid yellow centerlines prohibit passing in either direction.')]
for i,(key,prompt,correct,wrong,explanation) in enumerate(markings):
 q=dict(id=f'v{25+i:03}',module='lanes',page=132,section='4.16',prompt=prompt,choices=[correct,*wrong],answer=0,explanation=explanation,visual=key,visualQuestion=True)
 if not any(x['id']==q['id'] for x in c['questions']):c['questions'].append(q)
c['visuals']=visuals
f.write_text('window.CONTENT = '+json.dumps(c,ensure_ascii=False)+';\n')
# Contact sheet for verifying that captions have been excluded from the crops.
sheet=Image.new('RGB',(800,((len(thumbs)+5)//6)*165),'#edf2e8');d=ImageDraw.Draw(sheet)
for i,im in enumerate(thumbs):
 im.thumbnail((110,125));x=(i%6)*132+10;y=(i//6)*165+10;sheet.paste(im,(x,y));d.text((x,y+132),f'v{i+1:03}',fill='black')
sheet.save(root/'research/visual-crops.png')
print(len(c['questions']),'questions;',len(visuals),'embedded visual assets')
