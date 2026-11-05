// Ktizzle and Mattyrizz wedding site: saves RSVPs and advice to the Google Sheet,
// and serves the public advice wall. Paste into Extensions > Apps Script in the Sheet.
const SHEET_ID = '1Bmt4wWBL9qlt3elpy4__9ATjQR09fGFJBRpsAEXJF-g';

function clean(v) {
  const s = String(v == null ? '' : v).slice(0, 2000);
  return /^[=+\-@]/.test(s) ? "'" + s : s; // stop text being treated as a formula
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const d = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.openById(SHEET_ID);
    const now = new Date();
    if (d.type === 'rsvp') {
      ss.getSheetByName('RSVPs').appendRow([
        now, clean(d.name), clean(d.email), clean(d.attending), clean(d.days),
        Number(d.adults) || 0, Number(d.kids) || 0, Number(d.kidsSeats) || 0,
        clean(d.partyNames), clean(d.dietary), clean(d.songs), clean(d.lodging),
        clean(d.nights), clean(d.housing), clean(d.notes)
      ]);
    } else if (d.type === 'advice') {
      ss.getSheetByName('Advice').appendRow([
        now, clean(d.category), clean(d.advice), clean(d.name), d.showName === 'yes', false
      ]);
    }
    return json({ ok: true });
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  if (!e || !e.parameter || !e.parameter.wall) return json({ ok: true });
  const rows = SpreadsheetApp.openById(SHEET_ID).getSheetByName('Advice').getDataRange().getValues().slice(1);
  const items = rows
    .filter(r => r[2] && r[5] !== true)
    .reverse()
    .slice(0, 200)
    .map(r => ({ category: r[1], advice: r[2], name: r[4] === true ? r[3] : '' }));
  return json({ items: items });
}
