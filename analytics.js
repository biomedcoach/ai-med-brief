// AiMedbrief Analytics Tracker (local)
// POSTs page views & article clicks to http://localhost:5000
(function(){
  if(window._ab_tracked) return; window._ab_tracked=1;
  var TRACK_URL='http://localhost:5000';

  // Derive page path and article_id from <meta> tags or URL
  var metaPage=document.querySelector('meta[name="ab-page"]');
  var metaAid=document.querySelector('meta[name="ab-article-id"]');
  var page=metaPage?metaPage.content:(location.pathname.replace(/^\//,'')||'index.html');
  var aid=metaAid?metaAid.content:(page.match(/\\d{4}-\\d{2}-\\d{2}-(\\d+)\\.html/)||[])[1]||null;

  // Track page view
  fetch(TRACK_URL+'/track',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({page:page,article_id:aid,referrer:document.referrer||''})
  }).catch(function(){});

  // Track article card clicks (homepage only)
  document.querySelectorAll('.card-title a, .sb-item').forEach(function(el){
    el.addEventListener('click',function(){
      var href=el.getAttribute('href')||el.onclick&&el.onclick.toString().match(/articles\\/([^']+)/);
      var match=href&href[1]?href[1].match(/\\d{4}-\\d{2}-\\d{2}-(\\d+)/):null;
      if(match){
        fetch(TRACK_URL+'/track-click',{
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify({article_id:match[1],title:el.textContent.trim().substring(0,200)})
        }).catch(function(){});
      }
    });
  });
})();