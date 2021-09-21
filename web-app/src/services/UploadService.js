import http from '../http-common'

class UploadService {
  upload( file, onUploadProgress ) {
    let formData = new FormData()

    formData.append( 'imgfile', file )

    return http.post( '/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress
    } )
  }
}

export default new UploadService()