// --- Happy chime ---
// C-major arpeggio (C5 → E5 → G5) on sine oscillators with exponential
// decay. ~300 ms, gentle volume. Silent no-op if AudioContext is still
// suspended (no prior user gesture).
var _ivAudioCtx = null;

function playDoneSound() {
  try {
    var AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    if (!_ivAudioCtx) _ivAudioCtx = new AudioCtx();

    var ctx = _ivAudioCtx;
    if (ctx.state === 'suspended') { try { ctx.resume(); } catch(e) {} }

    var now = ctx.currentTime;
    var notes = [523.25, 659.25, 783.99]; // C5, E5, G5
    notes.forEach(function(freq, i) {
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.value = freq;

      var start = now + i * 0.09;
      var duration = 0.35;
      
      gain.gain.setValueAtTime(0.0001, start);
      gain.gain.exponentialRampToValueAtTime(0.16, start + 0.015);
      gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);
      osc.connect(gain).connect(ctx.destination);
      osc.start(start);
      osc.stop(start + duration + 0.02);
    });
  } catch(e) {}
}