import React, { useEffect } from "react";
import { Text, View, Button } from "react-native";
import api from "./src/services/api";

import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import ListeningScreen from "./src/screens/ListeningScreen";

const Stack = createNativeStackNavigator();

function HomeScreen({ navigation }) {
  return (
    <View style={{ marginTop: 60, padding: 20 }}>
      <Text style={{ fontSize: 20, marginBottom: 20 }}>
        Music Identification App 🎵
      </Text>

      <Button
        title="Start Listening"
        onPress={() => navigation.navigate("Listening")}
      />
    </View>
  );
}

export default function App() {
  useEffect(() => {
    api
      .get("/")
      .then((res) => {
        console.log("Backend says:", res.data);
      })
      .catch((err) => {
        console.log("Error:", err.message);
      });
  }, []);

  return (
    <NavigationContainer>
      <Stack.Navigator>

        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Listening" component={ListeningScreen} />

      </Stack.Navigator>
    </NavigationContainer>
  );
}
