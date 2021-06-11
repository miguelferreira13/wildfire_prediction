const AustraliaApiUrl = 'https://mapbox://styles/kryscage/ckpqorm1d026o19puj67p89ab/predict';

const AustraliaApiAppId = 'kryscage';
const AustraliaApiKey = 'https://api.mapbox.com/styles/v1/kryscage/ckpqorm1d026o19puj67p89ab.html?fresh=true&title=view&access_token=pk.eyJ1Ijoia3J5c2NhZ2UiLCJhIjoiY2twcWwzajE3MDh1YzJ2czhvdnI1bDBubCJ9.nAG4P8C2gctaVIhBhH3Z6w';

const mapboxApiToken = 'pk.eyJ1Ijoia3J5c2NhZ2UiLCJhIjoiY2twcWwzajE3MDh1YzJ2czhvdnI1bDBubCJ9.nAG4P8C2gctaVIhBhH3Z6w' ;

const displayMap = (start, stop) => {
    mapboxgl.accessToken = mapboxApiToken;
    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/satellite-streets-v11', // stylesheet location
        center: [133.58514407899872, -27.740477149652342], // starting position [lng, lat]
         zoom : 3.209581768010281
    });
