# -*- coding: utf-8 -*-
"""Patch de la demo : cockpit en vraie interface Airtable, ticket en vrai Jira.

N'edite pas le rendu existant : injecte un bloc CSS et un script de post-traitement
juste avant </body>. Rejouable, et retirable en supprimant le bloc marque.
"""
import pathlib, re, sys

CIBLE = sys.argv[1] if len(sys.argv) > 1 else "demo.html"
MARQUE = "<!-- PATCH-AIRTABLE-JIRA -->"

CSS = r"""
/* ============ 1 · FIDELITE AIRTABLE ============ */
.air{--at-blue:#2D7FF9;--at-line:#E5E5E5;--at-head:#F7F7F7;--at-hover:#F5F9FF;
     --at-txt:#1D1F25;--at-mut:#6B6F76}
@media (prefers-color-scheme:dark){.air{--at-line:#33322C;--at-head:#1F1E19;
     --at-hover:#232219;--at-txt:#EEEBDF;--at-mut:#9A988B}}

/* barre d'outils facon Airtable */
.at-bar{display:flex;align-items:center;gap:2px;padding:6px 10px;
  border-bottom:1px solid var(--at-line);flex-wrap:wrap;font-size:12.5px}
.at-bar button{appearance:none;background:transparent;border:0;border-radius:4px;
  padding:5px 9px;cursor:pointer;color:var(--at-txt);display:inline-flex;align-items:center;gap:6px;
  font:inherit;font-size:12.5px}
.at-bar button:hover{background:var(--at-hover)}
.at-bar svg{width:14px;height:14px;flex:none;opacity:.62}
.at-bar .at-sp{flex:1}
.at-bar .at-count{color:var(--at-mut);font-size:12px;padding-right:6px}

/* en-tetes de colonnes typees */
.airgrid th{position:relative;padding-left:26px!important;white-space:nowrap;
  background:var(--at-head)!important;text-transform:none!important;letter-spacing:0!important;
  font:600 12.5px var(--fb)!important;color:var(--at-txt)!important;border-right:1px solid var(--at-line)}
.airgrid th .ft{position:absolute;left:8px;top:50%;transform:translateY(-50%);
  width:13px;height:13px;opacity:.5}
.airgrid th .ft svg{width:13px;height:13px;display:block}

/* colonne de numero de ligne, figee a gauche */
.airgrid td.at-rn,.airgrid th.at-rn{position:sticky;left:0;z-index:3;width:44px;min-width:44px;
  padding:0 0 0 8px!important;background:var(--surface,#fff);color:var(--at-mut);
  font:500 11.5px var(--fm);border-right:1px solid var(--at-line);text-align:left}
.airgrid th.at-rn{background:var(--at-head)}
.airgrid tbody tr:hover td.at-rn{background:var(--at-hover)}
.airgrid td.at-rn .at-exp{display:none;margin-left:5px;border:1px solid var(--at-line);
  border-radius:3px;padding:1px 4px;font-size:10px;background:var(--surface,#fff);cursor:pointer}
.airgrid tbody tr:hover td.at-rn .at-exp{display:inline-block}

/* pills de select colorees */
.at-pill{display:inline-block;padding:2px 8px;border-radius:9px;font-size:11.5px;
  font-weight:500;line-height:1.5;white-space:nowrap}
.at-c-blue{background:#D8EEFF;color:#0B4E8A} .at-c-vert{background:#DDF5E4;color:#14663A}
.at-c-jaune{background:#FFF3C4;color:#6B5200} .at-c-rose{background:#FFE0E3;color:#8A1B2B}
.at-c-violet{background:#EAE2FF;color:#4B2D8F} .at-c-gris{background:#EDEDED;color:#43464C}
.at-c-orange{background:#FFE6CC;color:#8A4B00}
@media (prefers-color-scheme:dark){
 .at-c-blue{background:#16304D;color:#9CC8F5} .at-c-vert{background:#16351F;color:#93D8AD}
 .at-c-jaune{background:#3A3008;color:#E8D07A} .at-c-rose{background:#3D1A1F;color:#F0A5AE}
 .at-c-violet{background:#26193F;color:#BFA8F0} .at-c-gris{background:#2A2922;color:#B9B6AA}
 .at-c-orange{background:#3A2408;color:#E5B27A}}

/* pills existantes de la demo, restylees en selects Airtable */
.airgrid .cible,.airgrid .chip,.airgrid .ta-pill,.airgrid .st-pill{
  display:inline-block!important;padding:2px 9px!important;border-radius:9px!important;
  font:500 11.5px var(--fb)!important;line-height:1.55!important;letter-spacing:0!important;
  text-transform:none!important;border:0!important;white-space:nowrap}
.airgrid .cible.B2C{background:#D8EEFF!important;color:#0B4E8A!important}
.airgrid .cible.B2B{background:#EAE2FF!important;color:#4B2D8F!important}
.airgrid .chip.immo{background:#DDF5E4!important;color:#14663A!important}
.airgrid .chip.auto{background:#FFE6CC!important;color:#8A4B00!important}
.airgrid .chip.conso{background:#FFF3C4!important;color:#6B5200!important}
.airgrid .chip.b2b{background:#EAE2FF!important;color:#4B2D8F!important}
.airgrid .chip.sc{background:#EDEDED!important;color:#43464C!important}
.airgrid .ta-pill.creer{background:#DDF5E4!important;color:#14663A!important}
.airgrid .ta-pill.optimiser{background:#FFE6CC!important;color:#8A4B00!important}
.airgrid .st-pill.opp{background:#EDEDED!important;color:#43464C!important}
.airgrid .st-pill.prod{background:#D8EEFF!important;color:#0B4E8A!important}
.airgrid .st-pill.conf{background:#FFF3C4!important;color:#6B5200!important}
.airgrid .st-pill.val{background:#EAE2FF!important;color:#4B2D8F!important}
.airgrid .st-pill.pub{background:#DDF5E4!important;color:#14663A!important}
.airgrid .date-v{font:500 12.5px var(--fm)!important;color:var(--at-mut)}
@media (prefers-color-scheme:dark){
 .airgrid .cible.B2C,.airgrid .st-pill.prod{background:#16304D!important;color:#9CC8F5!important}
 .airgrid .cible.B2B,.airgrid .chip.b2b,.airgrid .st-pill.val{background:#26193F!important;color:#BFA8F0!important}
 .airgrid .chip.immo,.airgrid .ta-pill.creer,.airgrid .st-pill.pub{background:#16351F!important;color:#93D8AD!important}
 .airgrid .chip.auto,.airgrid .ta-pill.optimiser{background:#3A2408!important;color:#E5B27A!important}
 .airgrid .chip.conso,.airgrid .st-pill.conf{background:#3A3008!important;color:#E8D07A!important}
 .airgrid .chip.sc,.airgrid .st-pill.opp{background:#2A2922!important;color:#B9B6AA!important}}

/* avatar collaborateur */
.at-user{display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.at-av{width:19px;height:19px;border-radius:50%;background:var(--at-blue);color:#fff;
  font:600 9.5px var(--fb);display:inline-flex;align-items:center;justify-content:center;flex:none}

/* ligne d'ajout */
.airgrid td.at-rn .at-sub{display:inline-block;width:11px;height:1px;background:var(--at-line);
  margin-left:9px;vertical-align:middle}
.at-add td{padding:8px 12px!important;color:var(--at-mut);font-size:13px;cursor:default}
.at-add:hover td{background:var(--at-hover)}

/* ============ 2 · RENDU JIRA ============ */
.jira{--j-blue:#0052CC;--j-bg:#FFFFFF;--j-soft:#F4F5F7;--j-line:#DFE1E6;
  --j-txt:#172B4D;--j-mut:#6B778C;font-family:-apple-system,"Segoe UI",Roboto,Inter,sans-serif;
  color:var(--j-txt);border:1px solid var(--j-line);border-radius:4px;overflow:hidden;
  background:var(--j-bg);margin-top:12px}
.jira *{box-sizing:border-box}
.j-chrome{background:#F4F5F7;border-bottom:1px solid var(--j-line);padding:7px 12px;
  display:flex;align-items:center;gap:9px}
.j-dots{display:flex;gap:5px}.j-dots i{width:10px;height:10px;border-radius:50%;display:block}
.j-url{flex:1;background:#fff;border:1px solid var(--j-line);border-radius:4px;
  padding:3px 10px;font-size:11.5px;color:var(--j-mut);font-family:var(--fm)}
.j-body{padding:16px 18px 18px}
.j-crumb{font-size:12px;color:var(--j-mut);margin-bottom:9px}
.j-crumb b{color:var(--j-blue);font-weight:500}
.j-key{display:inline-flex;align-items:center;gap:7px;font-size:12.5px;color:var(--j-mut);
  font-weight:600;margin-bottom:6px}
.j-ic{width:16px;height:16px;border-radius:3px;display:inline-block;flex:none}
.j-ic.task{background:#4BADE8} .j-ic.story{background:#65BA43}
.j-title{font-size:23px;font-weight:600;line-height:1.25;margin:0 0 14px;color:var(--j-txt)}
.j-actions{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap}
.j-st{appearance:none;border:0;border-radius:3px;padding:6px 12px;font-size:13px;font-weight:600;
  cursor:default;display:inline-flex;align-items:center;gap:6px}
.j-st.todo{background:#DFE1E6;color:#42526E}
.j-st.prog{background:#DEEBFF;color:#0747A6}
.j-btn{appearance:none;border:0;border-radius:3px;padding:6px 12px;font-size:13px;
  background:var(--j-soft);color:var(--j-txt);cursor:default}
.j-cols{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:22px}
.j-h{font-size:12.5px;font-weight:600;color:var(--j-mut);margin:0 0 7px}
.j-desc{font-size:13.5px;line-height:1.58}
.j-desc p{margin:0 0 10px}
.j-desc h5{font-size:13.5px;font-weight:700;margin:14px 0 6px;color:var(--j-txt)}
.j-desc ul{margin:0 0 10px;padding-left:19px}
.j-desc li{margin-bottom:3px}
.j-panel{background:#DEEBFF;border-left:3px solid var(--j-blue);padding:10px 13px;
  border-radius:3px;margin:0 0 12px;font-size:13px}
.j-panel b{display:block;margin-bottom:3px}
.j-det{border:1px solid var(--j-line);border-radius:4px}
.j-det .j-dh{padding:8px 12px;border-bottom:1px solid var(--j-line);font-size:12.5px;
  font-weight:600;color:var(--j-mut);background:var(--j-soft)}
.j-row{display:grid;grid-template-columns:106px minmax(0,1fr);gap:10px;padding:7px 12px;font-size:13px}
.j-row span{color:var(--j-mut)}
.j-lab{display:inline-block;background:var(--j-soft);border-radius:3px;padding:2px 7px;
  font-size:11.5px;margin:0 4px 4px 0}
.j-usr{display:inline-flex;align-items:center;gap:6px}
.j-av{width:22px;height:22px;border-radius:50%;background:var(--j-blue);color:#fff;
  font-size:10px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;flex:none}
.j-foot{margin-top:14px;padding-top:11px;border-top:1px solid var(--j-line);
  font-size:12px;color:var(--j-mut)}
.j-note{font-size:12.5px;color:var(--muted);margin-top:10px}
@media (max-width:720px){.j-cols{grid-template-columns:1fr}}
"""

JS = r"""
(function(){
  /* ---------- types de champ Airtable ---------- */
  var ICO={
   text:'<svg viewBox="0 0 16 16"><path fill="currentColor" d="M2 3h12v1.6H9.1V13H6.9V4.6H2V3z"/></svg>',
   long:'<svg viewBox="0 0 16 16"><path fill="currentColor" d="M2 3h12v1.5H2V3zm0 3.5h12V8H2V6.5zM2 10h8v1.5H2V10z"/></svg>',
   num:'<svg viewBox="0 0 16 16"><path fill="currentColor" d="M5.6 2 5.1 5H2.4l-.2 1.5h2.7l-.4 3H1.8L1.6 11h2.7l-.5 3h1.5l.5-3h2.5l-.5 3h1.5l.5-3h2.6l.2-1.5h-2.6l.4-3h2.7l.2-1.5h-2.7l.5-3H9.8l-.5 3H6.8l.5-3H5.6zm1 4.5h2.5l-.4 3H6.2l.4-3z"/></svg>',
   sel:'<svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/><path fill="currentColor" d="M5.5 7.2 8 9.7l2.5-2.5-.9-.9L8 7.9 6.4 6.3z"/></svg>',
   date:'<svg viewBox="0 0 16 16"><rect x="2" y="3.2" width="12" height="11" rx="1.6" fill="none" stroke="currentColor" stroke-width="1.4"/><path stroke="currentColor" stroke-width="1.4" d="M2 6.6h12M5.4 1.8v2.6m5.2-2.6v2.6"/></svg>',
   user:'<svg viewBox="0 0 16 16"><circle cx="8" cy="5.4" r="2.7" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M2.9 14c0-2.6 2.3-4.2 5.1-4.2s5.1 1.6 5.1 4.2" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>',
   link:'<svg viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.5" d="M6.6 9.4a2.8 2.8 0 0 0 4 0l2.2-2.2a2.8 2.8 0 1 0-4-4l-1 1m-.4 2.4a2.8 2.8 0 0 0-4 0L1.2 8.8a2.8 2.8 0 1 0 4 4l1-1"/></svg>'
  };
  var TYPE={t:'long',kw:'text',vol:'num',score:'num',cible:'sel',rub:'sel',typeAction:'sel',
    st:'sel',title:'long',meta:'long',intention:'long',bloc:'long',topSource:'text',
    fanout:'long',hn:'long',serpEl:'text',majDate:'date',reoptDate:'date',briefDate:'date',
    livraisonDate:'date',resp:'user',tk:'link'};
  var COL={ /* libelle -> couleur de pill */
    'B2C':'blue','B2B':'violet','Immo':'vert','Actus Immo':'vert','Auto':'orange',
    'Actus Auto':'orange','Conso':'jaune','Astuces Maison':'jaune','B2B vertical':'violet',
    'À créer':'vert','À optimiser':'orange','créer':'vert','optimiser':'orange'};
  function pillCol(v){
    if(COL[v]) return COL[v];
    var s=(v||'').toLowerCase();
    if(s.indexOf('publi')>=0||s.indexOf('bon à publier')>=0) return 'vert';
    if(s.indexOf('relecture')>=0||s.indexOf('ar1')>=0||s.indexOf('ar2')>=0) return 'jaune';
    if(s.indexOf('rédaction')>=0||s.indexOf('production')>=0) return 'blue';
    if(s.indexOf('brief')>=0) return 'violet';
    if(s.indexOf('opportun')>=0||s.indexOf('scor')>=0) return 'gris';
    if(s.indexOf('optimis')>=0) return 'orange';
    return 'gris';
  }
  function initiales(n){return (n||'?').trim().split(/\s+/).map(function(m){return m[0];}).join('').slice(0,2).toUpperCase();}

  /* ---------- barre d'outils ---------- */
  function barre(){
    var air=document.querySelector('.air'); if(!air||air.querySelector('.at-bar'))return;
    var tools=air.querySelector('.air-tools'); if(!tools)return;
    var b=document.createElement('div'); b.className='at-bar';
    var items=[['Masquer les champs','long'],['Filtrer','sel'],['Grouper','num'],
               ['Trier','num'],['Couleur','sel'],['Hauteur de ligne','long']];
    b.innerHTML=items.map(function(it){
      return '<button type="button" tabindex="-1">'+ICO[it[1]]+it[0]+'</button>';}).join('')
      +'<span class="at-sp"></span><span class="at-count" id="atCount"></span>';
    tools.parentNode.insertBefore(b,tools);
  }

  /* ---------- post-traitement de la grille ---------- */
  var COLS=null;
  function typerEntetes(){
    var head=document.getElementById('airHead'); if(!head)return;
    var ths=head.querySelectorAll('th'); if(!ths.length)return;
    COLS=[];
    ths.forEach(function(th,i){
      if(th.classList.contains('at-rn'))return;
      if(th.querySelector('.ft'))return;
      var lib=(th.textContent||'').trim();
      var t=TYPE[th.dataset.col]||devine(lib);
      COLS.push(t);
      var s=document.createElement('span'); s.className='ft'; s.innerHTML=ICO[t]||ICO.text;
      th.insertBefore(s,th.firstChild);
    });
    if(!head.querySelector('.at-rn')){
      var rn=document.createElement('th'); rn.className='at-rn'; rn.textContent='';
      head.querySelector('tr').insertBefore(rn,head.querySelector('tr').firstChild);
    }
  }
  function devine(lib){
    var l=(lib||'').toLowerCase();
    if(/date|maj|livraison|ré-?opt/.test(l))return 'date';
    if(/volume|score|vol\b/.test(l))return 'num';
    if(/statut|cible|rubrique|action|type/.test(l))return 'sel';
    if(/resp|pilote|assign/.test(l))return 'user';
    if(/ticket|url|lien/.test(l))return 'link';
    if(/title|meta|intention|structure|question|bloc|sujet/.test(l))return 'long';
    return 'text';
  }
  function habillerLignes(){
    var body=document.getElementById('airBody'); if(!body)return;
    var n=0;
    Array.prototype.forEach.call(body.querySelectorAll('tr'),function(tr){
      if(tr.classList.contains('at-add'))return;
      if(tr.classList.contains('grouprow')){
        if(!tr.querySelector('.at-rn')){
          var tg=document.createElement('td'); tg.className='at-rn'; tg.textContent='';
          tr.insertBefore(tg,tr.firstChild);
        }
        return;
      }
      var enfant=tr.classList.contains('childrow');
      if(!enfant) n++;
      if(!tr.querySelector('.at-rn')){
        var td=document.createElement('td'); td.className='at-rn';
        td.innerHTML=enfant?'<span class="at-sub"></span>'
          :n+'<button class="at-exp" tabindex="-1" title="Ouvrir la fiche">⤢</button>';
        tr.insertBefore(td,tr.firstChild);
      }
      /* les selects de la demo sont deja balises (.cible, .chip, .ta-pill, .st-pill) :
         ils sont restyles en CSS, on ne touche pas au DOM. */
    });
    var sous=body.querySelectorAll('tr.childrow').length;
    var c=document.getElementById('atCount');
    if(c)c.textContent=n+(n>1?' enregistrements':' enregistrement')+(sous?' · '+(n+sous)+' requêtes avec les clusters':'');
    if(!body.querySelector('.at-add')){
      var cols=(document.getElementById('airHead')||{}).querySelectorAll?
        document.getElementById('airHead').querySelectorAll('th').length:8;
      var tr=document.createElement('tr'); tr.className='at-add';
      tr.innerHTML='<td class="at-rn">+</td><td colspan="'+Math.max(1,cols-1)+'">Ajouter un enregistrement</td>';
      body.appendChild(tr);
    }
  }
  function refresh(){ try{ barre(); typerEntetes(); habillerLignes(); }catch(e){} }

  var body=document.getElementById('airBody');
  if(body){ new MutationObserver(function(){refresh();}).observe(body,{childList:true}); }
  refresh();
  document.addEventListener('click',function(){setTimeout(refresh,60);},true);

  /* ---------- 2 · le ticket, en vrai Jira ----------
     ticketHTML() vit dans une IIFE : on ne peut pas la surcharger.
     On post-traite donc le DOM du modal quand le ticket s'affiche. */
  function champs(prev){
    var o={};
    Array.prototype.forEach.call(prev.querySelectorAll('.fld'),function(f){
      var b=f.querySelector('b'); if(!b)return;
      var lab=b.textContent.trim();
      var val=f.textContent.slice(lab.length).trim();
      if(lab && val) o[lab]=val;
    });
    return o;
  }
  function liste(txt,sep,max){
    if(!txt)return '';
    return txt.split(sep).map(function(x){return x.trim();}).filter(Boolean).slice(0,max||6)
      .map(function(x){return '<li>'+x+'</li>';}).join('');
  }
  function jiraHTML(card,prev){
    var c=champs(prev);
    var titre=(card.querySelector('h3')||{}).textContent||'';
    var kick=(card.querySelector('.b-kick')||card.querySelector('span')||{}).textContent||'';
    var rub=kick.split('·')[0]?kick.split('·')[0].trim():'';
    var cible=/B2B/.test(kick)?'B2B':'B2C';
    var obj=(card.querySelector('.obj')||{}).textContent||'';
    var resp=(obj.split('chez')[1]||'').trim()||'l\'équipe';
    var statut=(obj.match(/Statut\s*:\s*([^·]+)/)||[])[1]; statut=statut?statut.trim():'À faire';
    var n=0; for(var k=0;k<titre.length;k++) n=(n+titre.charCodeAt(k))%60;
    var cle='LBC-'+(240+n);
    var kwpb=c['Mot-clé prioritaire → page business']||'';
    var kw=kwpb.split('→')[0]?kwpb.split('→')[0].trim():'';
    var pb=kwpb.split('→')[1]?kwpb.split('→')[1].trim():'';
    var prio=/optimis/i.test(c["Type d'action"]||'')?'Moyenne':'Haute';
    var ini=(resp||'?').trim().split(/\s+/).map(function(m){return m[0];}).join('').slice(0,2).toUpperCase();
    return '<div class="jira"><div class="j-chrome"><div class="j-dots">'+
      '<i style="background:#FF5F57"></i><i style="background:#FEBC2E"></i><i style="background:#28C840"></i></div>'+
      '<div class="j-url">leboncoin.atlassian.net/browse/'+cle+'</div></div>'+
      '<div class="j-body">'+
      '<div class="j-crumb"><b>Projets</b> / <b>leboncoin Content</b> / '+cle+'</div>'+
      '<div class="j-key"><span class="j-ic task"></span>'+cle+'</div>'+
      '<h3 class="j-title">'+titre+'</h3>'+
      '<div class="j-actions"><button class="j-st todo">'+statut+'</button>'+
      '<button class="j-btn">Attribuer</button><button class="j-btn">Commenter</button></div>'+
      '<div class="j-cols"><div><p class="j-h">Description</p><div class="j-desc">'+
      '<div class="j-panel"><b>Brief-contrat, généré depuis le cockpit</b>'+
      'Ce ticket porte les champs du brief. Le critère de réussite est fixé avant l\'écriture et ne se rediscute plus.</div>'+
      (kw?'<h5>Mot-clé prioritaire</h5><p>'+kw+'</p>':'')+
      (pb?'<h5>Page business servie</h5><p>'+pb+'</p>':'')+
      (c['Intention SERP']?'<h5>Intention de recherche</h5><p>'+c['Intention SERP']+'</p>':'')+
      (c['Structure Hn (top 3)']?'<h5>Structure attendue, relevée sur le top 3</h5><ul>'+liste(c['Structure Hn (top 3)'],'·')+'</ul>':'')+
      (c['Questions à couvrir']?'<h5>Questions à couvrir</h5><ul>'+liste(c['Questions à couvrir'],'·')+'</ul>':'')+
      (c['Top sources à citer']?'<h5>Sources à citer</h5><p>'+c['Top sources à citer']+'</p>':'')+
      (c['Balise title']?'<h5>Balise title</h5><p>'+c['Balise title']+'</p>':'')+
      (c['Meta description']?'<h5>Meta description</h5><p>'+c['Meta description']+'</p>':'')+
      '</div></div><div>'+
      '<div class="j-det"><div class="j-dh">Détails</div>'+
      '<div class="j-row"><span>Type</span><div><span class="j-ic task" style="vertical-align:-3px"></span> Rédaction</div></div>'+
      '<div class="j-row"><span>Priorité</span><div>'+prio+'</div></div>'+
      '<div class="j-row"><span>Assigné à</span><div class="j-usr"><span class="j-av">'+ini+'</span>'+resp+'</div></div>'+
      '<div class="j-row"><span>Rapporteur</span><div class="j-usr"><span class="j-av" style="background:#6554C0">DS</span>cockpit datashake</div></div>'+
      '<div class="j-row"><span>Étiquettes</span><div><span class="j-lab">'+rub+'</span><span class="j-lab">'+cible+'</span>'+
        (c["Type d'action"]?'<span class="j-lab">'+c["Type d'action"].split('·')[0].trim()+'</span>':'')+'</div></div>'+
      '<div class="j-row"><span>Critère de réussite</span><div>présence sur la requête cible à 90 jours</div></div>'+
      '</div>'+
      '<div class="j-det" style="margin-top:12px"><div class="j-dh">Ressources du rédacteur</div>'+
      '<div class="j-row"><span>Espace</span><div>Corpus <span style="color:var(--j-mut)">· brief chargé</span></div></div>'+
      '<div class="j-row"><span>Cockpit</span><div>fiche liée, statut synchronisé</div></div>'+
      '</div></div></div>'+
      '<p class="j-foot">Ticket créé par le workflow n8n depuis le cockpit. Le cockpit reste la source de vérité, Jira reste l\'interface de vos équipes.</p>'+
      '</div></div>';
  }
  function destActive(card){
    var sw=card.querySelector('#destSw'); if(!sw)return null;
    var on=sw.querySelector('[aria-pressed="true"]');
    return on?(on.dataset.d||on.textContent.trim().toLowerCase()):null;
  }
  function majTicket(){
    var card=document.getElementById('modalCard'); if(!card)return;
    var prev=card.querySelector('.ticket-prev'); if(!prev)return;
    var d=destActive(card);
    var deja=card.querySelector('.jira');
    if(d==='jira'||/jira/i.test(d||'')){
      if(deja)return;
      prev.style.display='none';
      prev.insertAdjacentHTML('afterend', jiraHTML(card,prev));
    }else{
      if(deja){deja.parentNode.removeChild(deja); prev.style.display='';}
    }
  }
  var mc=document.getElementById('modalCard');
  if(mc){ new MutationObserver(function(){setTimeout(majTicket,30);})
            .observe(mc,{childList:true,subtree:true,attributes:true,attributeFilter:['aria-pressed']}); }
  document.addEventListener('click',function(){setTimeout(majTicket,120);},true);
})();
"""


def main():
    p = pathlib.Path(CIBLE)
    h = p.read_text(encoding="utf-8")
    # retire un patch precedent
    h = re.sub(re.escape(MARQUE) + r".*?" + re.escape("<!-- /PATCH -->"), "", h, flags=re.S)
    bloc = f"\n{MARQUE}\n<style>{CSS}</style>\n<script>{JS}</script>\n<!-- /PATCH -->\n"
    if "</body>" in h:
        h = h.replace("</body>", bloc + "</body>")
    else:
        h = h + bloc
    p.write_text(h, encoding="utf-8")
    print(f"{CIBLE} patche : +{len(bloc)/1024:.0f} Ko  (total {len(h)/1024:.0f} Ko)")


if __name__ == "__main__":
    main()
