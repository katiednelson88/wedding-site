// Rizz Airways site script
// After the Google Sheet script is deployed, paste its web app URL here.
var SITE_CONFIG = {
  endpoint: "https://script.google.com/macros/s/AKfycbyJDwtCjE74e8b39ti5a_V_Fvn1iiu9wh2mHhBMJkP1eY_5ZBHEma8mIJMtvxuLbB_Gxg/exec"
};

(function () {
  // Countdown
  var count = document.getElementById('count');
  if (count) {
    var target = new Date(2028, 4, 26);
    var now = new Date(); now.setHours(0, 0, 0, 0);
    var d = Math.round((target - now) / 86400000);
    count.textContent = d > 1 ? d + ' days' : d === 1 ? '1 day' : d === 0 ? 'Today!' : 'Married';
  }

  function send(payload) {
    if (!SITE_CONFIG.endpoint) return Promise.resolve('preview');
    return fetch(SITE_CONFIG.endpoint, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload)
    }).then(function () { return 'sent'; });
  }

  function showStatus(el, kind, msg) {
    el.hidden = false;
    el.className = 'status ' + kind;
    el.textContent = msg;
    el.focus && el.focus();
  }

  function checked(form, name) {
    return Array.prototype.map.call(form.querySelectorAll('input[name="' + name + '"]:checked'), function (i) { return i.value; });
  }

  // RSVP
  var rsvp = document.getElementById('rsvp-form');
  if (rsvp) {
    var lodgeBox = document.getElementById('lodge-details');
    var syncLodge = function () {
      var v = (rsvp.querySelector('input[name="lodging"]:checked') || {}).value;
      lodgeBox.hidden = v !== 'Lodges';
    };
    rsvp.addEventListener('change', syncLodge);
    syncLodge();

    rsvp.addEventListener('submit', function (e) {
      e.preventDefault();
      var errs = rsvp.querySelectorAll('.err');
      errs.forEach(function (x) { x.hidden = true; });
      var ok = true;
      function need(id, cond) { if (!cond) { document.getElementById(id).hidden = false; ok = false; } }
      need('err-name', rsvp.name.value.trim());
      need('err-email', /.+@.+\..+/.test(rsvp.email.value.trim()));
      var att = (rsvp.querySelector('input[name="attending"]:checked') || {}).value;
      need('err-attending', att);
      if (att && att !== 'No') need('err-days', checked(rsvp, 'days').length);
      if (!ok) { var first = rsvp.querySelector('.err:not([hidden])'); first && first.scrollIntoView({ block: 'center' }); return; }

      var payload = {
        type: 'rsvp',
        name: rsvp.name.value.trim(),
        email: rsvp.email.value.trim(),
        attending: att,
        days: checked(rsvp, 'days').join(', '),
        adults: rsvp.adults.value,
        kids: rsvp.kids.value,
        kidsSeats: rsvp.kidsSeats.value,
        partyNames: rsvp.partyNames.value.trim(),
        dietary: rsvp.dietary.value.trim(),
        songs: rsvp.songs.value.trim(),
        lodging: (rsvp.querySelector('input[name="lodging"]:checked') || {}).value || '',
        nights: checked(rsvp, 'nights').join(', '),
        housing: (rsvp.querySelector('input[name="housing"]:checked') || {}).value || '',
        bunkWith: rsvp.bunkWith.value.trim(),
        notes: rsvp.notes.value.trim()
      };
      var status = document.getElementById('rsvp-status');
      var btn = rsvp.querySelector('button[type=submit]');
      btn.disabled = true;
      send(payload).then(function (r) {
        if (r === 'preview') showStatus(status, 'warn', 'Preview mode: the form works, but it is not connected to the spreadsheet yet, so nothing was saved.');
        else { showStatus(status, 'ok', att === 'No' ? 'Got it. We will miss you! Thanks for letting us know.' : 'You are on the manifest! Thanks ' + payload.name.split(' ')[0] + ', we will be in touch.'); rsvp.reset(); syncLodge(); }
      }).catch(function () {
        showStatus(status, 'bad', 'That did not go through. Check your connection and try again, or text Katie or Matt.');
      }).then(function () { btn.disabled = false; });
    });
  }

  // Advice
  var advice = document.getElementById('advice-form');
  var wall = document.getElementById('wall');
  var esc = function (s) { var d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; };
  function card(item) {
    return '<article class="card"><span class="cat">' + esc(item.category) + '</span><p class="txt">' + esc(item.advice) + '</p>' +
      (item.name ? '<span class="who">&mdash; ' + esc(item.name) + '</span>' : '<span class="who">&mdash; Anonymous legend</span>') + '</article>';
  }
  function render(items) {
    if (!wall) return;
    if (!items.length) { wall.innerHTML = '<div class="wall-empty">No advice yet. Be the first wise one.</div>'; return; }
    wall.innerHTML = items.map(card).join('');
  }
  var examples = [
    { category: 'Example: day-of', advice: 'Eat something during cocktail hour. Trust me.', name: '' },
    { category: 'Example: marriage', advice: 'Take five minutes alone together right after the ceremony.', name: '' },
    { category: 'Example: planning', advice: 'Pick the three things you care about most and let the rest go.', name: '' },
    { category: 'Example: wildcard', advice: 'Pack a spare pair of socks. Scotland.', name: '' }
  ];
  if (wall) {
    if (!SITE_CONFIG.endpoint) render(examples);
    else fetch(SITE_CONFIG.endpoint + '?wall=1').then(function (r) { return r.json(); }).then(function (j) { render(j.items || []); }).catch(function () { render([]); });
  }
  if (advice) {
    advice.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = document.getElementById('err-advice');
      err.hidden = !!advice.advice.value.trim();
      if (!err.hidden) return;
      var payload = {
        type: 'advice',
        category: advice.category.value,
        advice: advice.advice.value.trim(),
        name: advice.name.value.trim(),
        showName: advice.showName.checked ? 'yes' : 'no'
      };
      var status = document.getElementById('advice-status');
      var btn = advice.querySelector('button[type=submit]');
      btn.disabled = true;
      send(payload).then(function (r) {
        if (r === 'preview') showStatus(status, 'warn', 'Preview mode: not connected to the spreadsheet yet, so this was not saved.');
        else {
          showStatus(status, 'ok', 'Wisdom received. Thank you!');
          if (wall) {
            var html = card({ category: payload.category, advice: payload.advice, name: payload.showName === 'yes' ? payload.name : '' });
            if (wall.querySelector('.wall-empty')) wall.innerHTML = '';
            wall.insertAdjacentHTML('afterbegin', html);
          }
          advice.reset();
        }
      }).catch(function () {
        showStatus(status, 'bad', 'That did not go through. Try again in a minute.');
      }).then(function () { btn.disabled = false; });
    });
  }
})();
