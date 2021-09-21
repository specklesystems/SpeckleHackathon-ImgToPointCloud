<template>
  <v-container>
    <v-row class="mt-12">
      <v-file-input
        :rules="rules"
        accept="image/png, image/jpeg, image/bmp"
        placeholder="Select Images"
        prepend-icon="mdi-camera"
        background-color="light-blue lighten-5"
        solo
        flat
        rounded
        @change="selectFile"
        label="Images">
        <template #append>
            <v-btn
                rounded
                color="info"
                @click="upload">
            Upload
            </v-btn>
        </template>
      </v-file-input>
    </v-row>
    <v-row>
      <v-alert
      v-if="streamUrl != null"
      text
      color="light-blue"
      >
        <h3 class="text-h5">
          Generated Stream
        </h3>
        <div>Your point cloud has been generated from your images. View your results here!</div>

        <v-divider
          class="my-4 info"
          style="opacity: 0.22"
        ></v-divider>

        <v-row
          align="center"
          no-gutters
        >
          <v-col class="grow">
            <v-text-field
              v-model="streamUrl"
              dense
              filled
              rounded
              readonly
            ></v-text-field>
            <div>
            </div>
          </v-col>
          <v-spacer></v-spacer>
          <v-col class="shrink">
            <v-btn
              color="info"
              :href="streamUrl"
              target="_blank"
              rounded
            >
              Open
            </v-btn>
          </v-col>
        </v-row>
      </v-alert>
    </v-row>
  </v-container>
</template>

<script>
  import UploadService from '../services/UploadService'

  export default {
    name: 'Home',
    data: () => ( {
      currentFile: null,
      streamUrl: null,
      progress: 0
    } ),
    watch: {
    },
    methods: {
      selectFile( file ) {
        this.currentFile = file,
        this.progress = 0
      },

      upload() {
        if ( this.currentFile.length === 0 ) {
          return
        }

        UploadService.upload( this.currentFile, ( event ) => {
          this.progress = Math.round( ( 100 * event.loaded ) / event.total )
        } )
          .then( ( response ) => {
            this.streamUrl = 'hello world'
            return response
          } )
          .catch( ( ) => {
            this.progress = 0
            this.currentFile = undefined
          } )
      },

      mounted( ) {
        UploadService.getStream( ).then( response => {
          this.streamUrl = response.data
        } )
      }

    },
    computed: {
      
    }
  }
</script>
