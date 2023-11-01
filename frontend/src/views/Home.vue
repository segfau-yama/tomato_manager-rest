<template>
  <v-app>
    <v-container>
      <div class="text-center">
        <h1>{{ crop[level.maturity - 1] }}</h1>
        <v-icon size="400px" :color="color[level.maturity - 1]"
          >mdi-food-apple</v-icon
        >
        <v-slider
          v-model="level.maturity"
          :min="1"
          :max="5"
          :step="1"
          class="ma-5"
          label="レベル"
          thumb-label
          show-ticks="always"
          tick-size="4"
        ></v-slider>
        <v-btn class="info" @click="do_post">成熟度を送信</v-btn>
      </div>
    </v-container>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  data() {
    return {
      color: ["#00FF00", "#FFFF00", "#FF0000", "#FFA500", "#0000FF"],
      level: {
        maturity: 1,
        date_time: new Date(),
      },
      crop: ["green_apple", "yellow_apple", "red_apple", "orange", "tomato"],
    };
  },
  methods: {
    do_post() {
      const now = new Date()
      this.level.date_time = now
      const url: string = 'http://127.0.0.1:8000/level/level/'
      this.axios.post(url, this.level)
    }
  },
});
</script>
