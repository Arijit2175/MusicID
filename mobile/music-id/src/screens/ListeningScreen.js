import React, { useEffect, useState } from "react";
import { View, Text } from "react-native";
import { startAudioStream, stopAudioStream } from "../services/audioEngine";

export default function ListeningScreen() {
  const [level, setLevel] = useState(0);

  useEffect(() => {
    startAudioStream((amplitude) => {
      setLevel(amplitude);
    });

    return () => stopAudioStream();
  }, []);

  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>Listening...</Text>
      <Text>Audio Level: {level}</Text>
    </View>
  );
}
