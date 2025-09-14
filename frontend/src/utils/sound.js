// Simple notification sound using Web Audio API
// Creates a short beep when invoked. Gracefully no-ops if audio is blocked.

let sharedAudioContext = null;

function getAudioContext() {
  if (typeof window === 'undefined') return null;
  const AudioContextCtor = window.AudioContext || window.webkitAudioContext;
  if (!AudioContextCtor) return null;
  if (!sharedAudioContext) {
    sharedAudioContext = new AudioContextCtor();
  }
  return sharedAudioContext;
}

export async function playNotificationSound() {
  const audioContext = getAudioContext();
  if (!audioContext) return;

  try {
    if (audioContext.state === 'suspended') {
      // Attempt to resume; may fail without user gesture but that's okay
      await audioContext.resume();
    }

    const durationSeconds = 0.15;
    const attackSeconds = 0.005;
    const decaySeconds = 0.12;
    const frequencyHz = 880;

    const now = audioContext.currentTime;
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();

    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(frequencyHz, now);

    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.4, now + attackSeconds);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + attackSeconds + decaySeconds);

    oscillator.connect(gain);
    gain.connect(audioContext.destination);

    oscillator.start(now);
    oscillator.stop(now + durationSeconds);
  } catch (e) {
    // Ignore errors related to autoplay policies
    // eslint-disable-next-line no-console
    console.debug('Notification sound blocked or failed:', e);
  }
}


