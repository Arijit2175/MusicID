import { Audio } from "expo-av";

let recording = null;

export async function startAudioStream(onData) {
  try {
    await Audio.requestPermissionsAsync();

    await Audio.setAudioModeAsync({
      allowsRecordingIOS: true,
      playsInSilentModeIOS: true,
    });

    recording = new Audio.Recording();
    
    await recording.prepareToRecordAsync(
      Audio.RecordingOptionsPresets.HIGH_QUALITY
    );

    recording.setOnRecordingStatusUpdate((status) => {
      if (status.isRecording && onData) {
        onData(status.metering);
      }
    });

    await recording.startAsync();
    return true;

  } catch (error) {
    console.log("Audio Stream Error:", error);
    return false;
  }
}

export async function stopAudioStream() {
  try {
    if (!recording) return;

    await recording.stopAndUnloadAsync();
    recording = null;
  } catch (error) {
    console.log("Stop Stream Error:", error);
  }
}
