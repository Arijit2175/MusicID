import React, { useEffect } from "react";
import { Text, View } from "react-native";
import api from "./src/services/api";

export default function App() {
  useEffect(() => {
    api.get("/").then(res => {
      console.log("Backend says:", res.data);
    }).catch(err => {
      console.log("Error:", err.message);
    });
  }, []);

  return (
    <View style={{ marginTop: 60 }}>
      <Text>Music Identification App 🎵</Text>
    </View>
  );
}
