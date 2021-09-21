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
      <v-col>
        <v-progress-linear
          v-if=progressLoading
          indeterminate
        ></v-progress-linear>
      </v-col>
    </v-row>
    <v-row>
      <v-alert
      v-if="finishedLoading"
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
      <v-alert
      v-if="alert"
      outlined
      color="warning"
      prominent
      dismissible>
        Could not generate point cloud :(
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
      progressLoading: false,
      finishedLoading:false,
      alert: false
    } ),
    watch: {
    },
    methods: {
      selectFile( file ) {
        this.currentFile = file,
        this.progressLoading = false,
        this.finishedLoading = false
        this.alert = false
      },

      upload() {
        if ( this.currentFile.length === 0 ) {
          return
        }
        this.progressLoading = true
        this.alert = false

        UploadService.upload( this.currentFile, ( event ) => {
        } )
          .then( ( response ) => {
            this.streamUrl = response.data
            this.progressLoading = false
            this.finishedLoading = true
            return response
          } )
          .catch( ( ) => {
            this.alert = true
            this.progressLoading = false
            this.currentFile = undefined
            this.finishedLoading = false
          } )
      },

      mounted( ) {
        UploadService.getStream( ).then( response => {
          this.streamUrl = response.data
          this.progressLoading = false
          this.finishedLoading = false
          this.alert = false
        } )
      }

    },
    computed: {
      
    }
  }
</script>
