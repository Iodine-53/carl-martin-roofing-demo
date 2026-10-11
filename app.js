/* Carl Martin Roofing demo — stepper, FAQ, clock, callbar, reveals */
(function(){
"use strict";
document.documentElement.classList.add('js');

var $ = function(s,c){ return (c||document).querySelector(s); };
var $$ = function(s,c){ return Array.prototype.slice.call((c||document).querySelectorAll(s)); };

/* ---------- mobile nav ---------- */
var toggle = $('.nav-toggle'), mnav = $('#mobile-nav');
if(toggle){
  toggle.addEventListener('click', function(){
    var open = mnav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  $$('#mobile-nav a').forEach(function(a){
    a.addEventListener('click', function(){ mnav.classList.remove('open'); toggle.setAttribute('aria-expanded','false'); });
  });
}

/* ---------- 4-step inspection stepper ---------- */
var form = $('.stepper');
if(form){
  var steps = $$('.step', form), dots = $$('.step-dots li'), fill = $('#progress-fill'),
      prog = $('#step-progress'), nextBtn = $('#step-next'), backBtn = $('#step-back'),
      current = 0,
      state = { service:'', zip:'', size:'', time:'' };

  function setStep(n){
    current = n;
    steps.forEach(function(s,i){ s.classList.toggle('active', i===n); });
    dots.forEach(function(d,i){
      d.classList.toggle('active', i===n);
      d.classList.toggle('done', i<n);
      var chk = $('.dot-check', d);
      if(chk) chk.hidden = !(i<n);
    });
    var pct = ((n+1)/steps.length)*100;
    fill.style.width = pct + '%';
    prog.setAttribute('aria-valuenow', n+1);
    backBtn.hidden = (n===0);
    nextBtn.textContent = (n===steps.length-1) ? 'Book my inspection' : 'Continue';
    steps[n].querySelector('.step-q').focus && steps[n].querySelector('.step-q').setAttribute('tabindex','-1');
  }

  $$('.chip', form).forEach(function(chip){
    chip.addEventListener('click', function(){
      var field = chip.getAttribute('data-field');
      $$('.chip[data-field="'+field+'"]', form).forEach(function(c){ c.setAttribute('aria-pressed','false'); });
      chip.setAttribute('aria-pressed','true');
      state[field] = chip.getAttribute('data-value');
      /* auto-advance one beat after choosing, like a real booking flow */
      setTimeout(function(){ if(current<steps.length-1) setStep(current+1); }, 320);
    });
  });

  var zipInput = $('#zip');
  function zipOk(){ return /^[0-9]{5}$/.test((zipInput.value||'').trim()); }
  zipInput.addEventListener('input', function(){ state.zip = zipInput.value.trim(); });

  nextBtn.addEventListener('click', function(){
    if(current===0 && !state.service){ nudge('Pick what you need first.'); return; }
    if(current===1 && !zipOk()){ nudge('Enter your 5-digit Tampa ZIP.'); zipInput.focus(); return; }
    if(current===2 && !state.size){ nudge('Pick a home size — "not sure" is fine.'); return; }
    if(current===3){
      if(!state.time){ nudge('Pick a callback time.'); return; }
      composeMail(); return;
    }
    setStep(current+1);
  });
  backBtn.addEventListener('click', function(){ if(current>0) setStep(current-1); });

  function nudge(msg){
    var q = steps[current].querySelector('.step-q');
    q.setAttribute('tabindex','-1'); q.focus({preventScroll:false});
    var old = q.textContent; q.textContent = msg;
    setTimeout(function(){ q.textContent = old; }, 1600);
  }

  function composeMail(){
    var body = 'Free roof inspection request%0D%0A%0D%0A' +
      'Service: ' + encodeURIComponent(state.service) + '%0D%0A' +
      'ZIP: ' + encodeURIComponent(state.zip) + '%0D%0A' +
      'Home size: ' + encodeURIComponent(state.size) + '%0D%0A' +
      'Call me: ' + encodeURIComponent(state.time) + '%0D%0A';
    window.location.href = 'mailto:roofinone@aol.com?subject=' +
      encodeURIComponent('Free inspection request — ' + state.service + ', ' + state.zip) +
      '&body=' + body;
  }
  setStep(0);
}

/* ---------- FAQ accordion ---------- */
$$('.faq-item button').forEach(function(btn){
  btn.addEventListener('click', function(){
    var open = btn.getAttribute('aria-expanded') === 'true';
    var panel = document.getElementById(btn.getAttribute('aria-controls'));
    btn.setAttribute('aria-expanded', open ? 'false' : 'true');
    panel.hidden = open;
  });
});

/* ---------- live Tampa clock + open chip ---------- */
function tick(){
  try{
    var t = new Date(new Date().toLocaleString('en-US',{timeZone:'America/New_York'}));
    var el = $('#local-time');
    if(el) el.textContent = t.toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit'});
    var chip = $('#open-chip'), h = t.getHours(), dow = t.getDay();
    if(chip){
      if(h>=7 && h<19 && dow!==0){ chip.textContent = 'OPEN NOW · on call till 7 PM'; }
      else { chip.textContent = 'Next inspections 8 AM'; }
    }
  }catch(e){/* static fallback stays */}
}
tick(); setInterval(tick, 30000);

/* ---------- sticky mobile callbar: up after hero, gone at final CTA ---------- */
var callbar = $('#callbar');
if(callbar && 'IntersectionObserver' in window){
  var hero = $('.hero'), finalCta = $('.final'), booking = $('#booking');
  var pastHero = false, atFinal = false, atBooking = false;
  function render(){ callbar.classList.toggle('show', pastHero && !atFinal && !atBooking); }
  new IntersectionObserver(function(e){ pastHero = !e[0].isIntersecting && e[0].boundingClientRect.top < 0; render(); },{threshold:0}).observe(hero);
  new IntersectionObserver(function(e){ atFinal = e[0].isIntersecting; render(); },{threshold:0.08}).observe(finalCta);
  if(booking) new IntersectionObserver(function(e){ atBooking = e[0].isIntersecting; render(); },{threshold:0.25}).observe(booking);
}

/* ---------- reveals: blur-to-sharp headlines, wipe photos (observe wrappers) ---------- */
if('IntersectionObserver' in window){
  $$('h1,h2').forEach(function(h){ h.classList.add('rv'); });
  $$('.livejob-fig img,.tl-item img,.ba-pair img,.tech-card img').forEach(function(im){ im.classList.add('wipe'); });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
    });
  },{threshold:0.12, rootMargin:'0px 0px 25% 0px'});
  $$('.rv').forEach(function(el){ io.observe(el); });
  $$('.livejob-fig,.tl-item figure,.tl-item,.ba-pair figure,.tech-card').forEach(function(wrap){
    io.observe(wrap);
    /* mark contained wipe targets when wrapper enters */
    new IntersectionObserver(function(es,obs){
      es.forEach(function(x){ if(x.isIntersecting){ $$('.wipe',x.target).forEach(function(i){i.classList.add('in');}); obs.disconnect(); } });
    },{threshold:0, rootMargin:'0px 0px 25% 0px'}).observe(wrap);
  });
  /* no-interaction backstop: everything readable by 3s, whatever IO says */
  setTimeout(function(){
    $$('.rv:not(.in)').forEach(function(el){ el.classList.add('in'); });
    $$('.wipe:not(.in)').forEach(function(el){ el.classList.add('in'); });
  }, 3000);
}

/* ---------- footer year ---------- */
var fy = $('#foot-year'); if(fy) fy.textContent = new Date().getFullYear();
})();
