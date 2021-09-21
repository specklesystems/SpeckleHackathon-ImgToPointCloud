<template>
  <v-container>
    <v-row class="mt-12">
      <v-text-field
        label="commit url"
        flat
        rounded
        background-color="light-blue lighten-5"
        solo
        v-model="URL">
        <template #append>
            <v-btn
                rounded
                color="blue"
                @click="getObjects">
            get
            </v-btn>
        </template>
      </v-text-field>
    </v-row>
    <v-row>
      <v-col>
        <v-card
          max-width="300px"
        >
          <v-sheet class="pa-4 blue">
            <v-text-field
              v-model="search"
              label="Search Properties"
              dark
              flat
              solo-inverted
              hide-details
            ></v-text-field>
          </v-sheet>
          <v-card-text>
            <v-treeview
              selectable
              return-object
              v-model="filteredHeaders"
              :items="unflattenedHeaders"
            ></v-treeview>
          </v-card-text>
        </v-card>
        
      </v-col>
      <v-col>
        <v-text-field label="Limit" v-model.number="limit" type="number"></v-text-field>
        <v-data-table
          v-if="URL && URL.length !== 0"
          dense
          :headers="showHeaders"
          :items="flattenedObjects"
          :items-per-page="limit"
          :hide-default-footer="true"
          disable-sort
          class="elevation-1 mt-12">
        </v-data-table>
        <v-btn @click="prev" :loading='prevLoading' :disabled="cursors.length <= 2" class="mr-2">prev</v-btn>
        <v-btn @click="next" :loading='nextLoading' :disabled="cursors.length === 0 || (cursors.length - 1) * limit >= totalCount" class="mr-2">next</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import flatten from 'flat' 

  export default {
    name: 'Home',
    data: () => ( {
      URL: 'https://speckle.xyz/streams/5dfbeb49c9/commits/22bb89b5b8',
      totalCount: null,
      cursors: [],
      limit: 10,
      fetchLoading: false,
      prevLoading: false,
      nextLoading: false,
      flattenedObjects: [],
      headers: [],
      unflattenedHeaders: [],
      filteredHeaders:[]
    } ),
    watch: {
      limit() {
        // If the limit is changed, we need to reset the query
        this.getObjects()
      }
    },
    methods: {
      async next() {
        this.nextLoading = true
        await this.getObjects( false, this.cursors[ this.cursors.length - 1 ] )
        this.nextLoading = false
      },
      async prev() {
        this.prevLoading = true
        await this.cursors.pop() // remove last cursor
        await this.getObjects( false, this.cursors[ this.cursors.length - 2 ], false ) // fetch using the second last cursor
        this.prevLoading = false
      },
      async getObjects( cleanCursor = true, cursor = null, appendCursor = true ) {

        // get the stream and commit id from the url
        const url = new URL( this.URL )
        let pathArray = url.pathname.split( '/' )
        const streamId = pathArray[2]
        const commitId = pathArray[4]

        // create a query for the referenced object of this commit base
        const commitQuery = this.commitQuery( streamId, commitId )

        // fetch
        let commitRawRes = await fetch( new URL( '/graphql', url.origin ), {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify( {
            query: commitQuery,
            variables: { }
          } )
        } )

        let commitRes = await commitRawRes.json()
        let objectId = commitRes.data.stream.commit.referencedObject

        // create a query for graphql for all children of the commit
        const objectsQuery = this.objectsQuery( streamId, objectId, cursor )

        // fetch
        let objectsRawRes = await fetch( new URL( '/graphql', url.origin ), {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify( {
            query: objectsQuery,
            variables: { 
              limit: this.limit,
              mySelect: this.select ? JSON.parse( this.select ) : null, 
              myQuery: this.query ? JSON.parse( this.query ) : null
            }
          } )
        } )

        let objectsRes = await objectsRawRes.json()
        let children = objectsRes.data.stream.object.children

        // handle cursor pagination
        this.totalCount = children.totalCount
        if( cleanCursor ) this.cursors = [ null ]
        if( appendCursor ) this.cursors.push( children.cursor ) 

        // flatten these objects to generate table rows. 
        // This will still yield key value pairs in flattened json
        this.flattenedObjects = children.objects.map( o => flatten( o ) )

        // get the unique keys of flattened objects for the headers
        // then create headers with text and value
        let uniqueHeaders = new Set()
        this.flattenedObjects.forEach( o => Object.keys( o ).forEach( o => uniqueHeaders.add( o ) ) )
        uniqueHeaders.forEach( o => this.headers.push( { text: o, value: o, sortable:false } ) )

        // unflatten the headers to generate tree
        let headerTree = this.makeTreeFromHeaders( uniqueHeaders )
        this.unflattenedHeaders = headerTree
      },

      makeTreeFromHeaders( uniqueHeaders ) {
        let tree = [ { id: 0, name: 'all fields', fullname: '', children: [] } ]
        let i = 1
        for ( let header of uniqueHeaders ) {
          let parts = header.split( '.' )
          let leaf = tree[0].children
          let partIndex = 1
          for ( let part of parts ) {
            let index = leaf.findIndex( ( x ) => x.name === part )
            if ( index === -1 ) {
              let fullname = parts.slice( 0, partIndex ).join( '.' )
              leaf.push( { id: i, name: part, fullname: fullname, children: [] } )
              index = leaf.length - 1
              i++
            }
            partIndex++
            leaf = leaf[index].children
          }
        }
        return tree
      },

      objectsQuery( streamId, objectId, cursor = null ) {
      return `
        query ($limit: Int, $mySelect: [String!], $myQuery: [JSONObject!]) {
          stream( id: "${streamId}" ) {
            object( id: "${objectId}" ) {
              children ( 
                limit: $limit
                depth: 100
                select: $mySelect
                query: $myQuery
                ${ cursor ? ', cursor:"' + cursor + '"' : '' }
                ) {
                totalCount
                cursor
                objects {
                  data
                }
              }
            }
          }
        }
      `
      },

      commitQuery( streamId, commitId ) {
      return `
        query {
          stream( id: "${streamId}" ) {
            commit( id: "${commitId}" ) {
              referencedObject
            }
          }
        }
      `
      }


    },
    computed: {
      showHeaders () {
        let headersToRemove = []
        this.filteredHeaders.forEach( o => headersToRemove.push( o.fullname ) )
        let shownHeaders = this.headers.filter( s => !headersToRemove.includes( s.text ) )
        return shownHeaders
      }
    }
  }
</script>
