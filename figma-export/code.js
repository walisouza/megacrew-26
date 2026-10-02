figma.showUI(__html__, {width: 700, height: 520});
const props = ['id','name','type','visible','opacity','width','height','rotation','fills','strokes','strokeWeight','strokeAlign','effects','blendMode','cornerRadius','clipsContent','layoutMode','primaryAxisAlignItems','counterAxisAlignItems','itemSpacing','paddingTop','paddingBottom','paddingLeft','paddingRight','characters','textCase','textDecoration','textAlignVertical','fontName','fontSize','fontWeight','textAlignHorizontal','textAutoResize','lineHeight','letterSpacing','paragraphSpacing','hyperlink','reactions'];
let root;
function serialize(n) {
  const o = {};
  for (const k of props) {
    try { const v=n[k]; if(v!==undefined && typeof v!=='symbol') o[k]=v; } catch(e) {}
  }
  for(const k of ['absoluteBoundingBox','absoluteRenderBounds','absoluteTransform']) { try {o[k]=n[k];}catch(e){} }
  if(n.type==='TEXT') {
    try {o.segments=n.getStyledTextSegments(['fontName','fontSize','fontWeight','fills','lineHeight','letterSpacing','textDecoration','hyperlink']);}catch(e){o.segmentError=String(e)}
  }
  if('children' in n) o.children=n.children.map(serialize);
  return o;
}
(async()=> {
  root=await figma.getNodeByIdAsync('855:28');
  if(!root) root=figma.currentPage.findOne(n=>n.type==='FRAME' && n.name==='MEGACREW-REFORMA');
  if(!root) throw new Error('Frame MEGACREW-REFORMA não encontrado');
  figma.ui.postMessage({type:'metadata',data:serialize(root)});
})().catch(e=>figma.ui.postMessage({type:'error',message:String(e)}));
figma.ui.onmessage=async m=> {
  if(m.type!=='export') return;
  try {
    const assets=[];
    for(const id of m.ids) {
      const n=await figma.getNodeByIdAsync(id);
      if(!n) continue;
      figma.ui.postMessage({type:'progress',message:n.name+' ('+(assets.length+1)+'/'+m.ids.length+')'});
      const format=m.format||'SVG';
      const bytes=await n.exportAsync(format==='SVG'?{format:'SVG',svgOutlineText:true}:{format:'PNG',constraint:{type:'SCALE',value:1}});
      assets.push({id:n.id,name:n.name,format,bbox:n.absoluteBoundingBox,renderBounds:n.absoluteRenderBounds,bytes});
    }
    figma.ui.postMessage({type:'assets',assets});
  } catch(e) {figma.ui.postMessage({type:'error',message:String(e)+'\n'+e.stack});}
};
