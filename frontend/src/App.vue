<template>
  <v-app>
    <v-app-bar app scroll-behavior="hide">
      <v-toolbar-title>Tomato-manager</v-toolbar-title>
      <template v-slot:extension>
        <v-tabs v-model="tab" show-arrows app>
          <v-tab v-for="(page, index) in pages" :key="index" :to="page.path">
            {{ page.name }}
          </v-tab>
        </v-tabs>
      </template>
    </v-app-bar>

    <v-main>
      <RouterView></RouterView>
    </v-main>

    <v-footer></v-footer>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { pages } from '@/router'

export default defineComponent({
  name: 'App',
  data () {
    return {
      tab: null,
      search_icon: false,
      pages,
    }
  },
  methods: {
    on_search() {
      this.search_icon = !this.search_icon;
    }
  }
})
</script>
