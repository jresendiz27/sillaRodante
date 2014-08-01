package mx.devf.alemolina.condesaaccesible;

import android.os.AsyncTask;
import android.util.Log;

import com.google.android.gms.maps.model.LatLng;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by alemolina on 7/22/14.
 */
public class GetPointsInRoute extends AsyncTask<LatLng, Integer, RouteResult> {
    private String httpResponse = null;

    protected interface OnPathListener {
        public void latLngReady(RouteResult routeResult);
    }

    private OnPathListener listener;

    public void setListener(OnPathListener listener) {
        this.listener = listener;
    }

    @Override
    protected RouteResult doInBackground(LatLng... latlngs) {
        return postData(latlngs[0], latlngs[1]);
    }

    protected void onPostExecute(RouteResult result) {
        listener.latLngReady(result);
    }

    protected void onProgressUpdate(Integer... progress) {
        //pb.setProgress(progress[0]);
    }

    //"http://pepo27devf.appspot.com/obtenerRutas"
    public RouteResult postData(LatLng origin, LatLng destination) {
        // Create a new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost("http://pepo27devf.appspot.com/obtenerRutas");

        try {
            // Add your data
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();

            nameValuePairs.add(new BasicNameValuePair("latitudOrigen", "" + origin.latitude));
            nameValuePairs.add(new BasicNameValuePair("longitudOrigen", "" + origin.longitude));
            nameValuePairs.add(new BasicNameValuePair("latitudDestino", "" + destination.latitude));
            nameValuePairs.add(new BasicNameValuePair("longitudDestino", "" + destination.longitude));

            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

            Log.e(MainActivity.TAG, "URL: " + httppost.getURI());

            // Execute HTTP Post Request
            HttpResponse response = httpclient.execute(httppost);

            String responseString = new BasicResponseHandler().handleResponse(response);

            Log.e(MainActivity.TAG, "JSON Result: " + responseString);

            JSONObject jsonRoute = new JSONObject(responseString);


            JSONArray keyPoints = jsonRoute.getJSONArray("puntosClave");

            ArrayList<PlaceDot> placeDots = new ArrayList<PlaceDot>();
            for (int i = 0; i < keyPoints.length(); i++) {

                JSONObject keyPoint = keyPoints.getJSONObject(i);

                double longitud = keyPoint.getDouble("longitud");
                double latitud = keyPoint.getDouble("latitud");
                int score = keyPoint.getInt("tipo");

                PlaceDot placeDot = new PlaceDot();
                placeDot.setScore(score);
                placeDot.setPlace(new LatLng(latitud, longitud));

                placeDots.add(placeDot);

            }


            JSONObject possibleRoutes = jsonRoute.getJSONObject("rutaPropuesta");
            JSONArray routes = possibleRoutes.getJSONArray("routes");
            JSONObject firstRoute = routes.getJSONObject(0);
            JSONObject overviewPolyline = firstRoute.getJSONObject("overview_polyline");
            String encodedPolyline = overviewPolyline.getString("points");

            ArrayList<LatLng> route = decodePoly(encodedPolyline);

            JSONObject possibleRoutes2 = jsonRoute.getJSONObject("rutaMaps");
            JSONArray routes2 = possibleRoutes2.getJSONArray("routes");
            JSONObject firstRoute2 = routes2.getJSONObject(0);
            JSONObject overviewPolyline2 = firstRoute2.getJSONObject("overview_polyline");
            String encodedPolyline2 = overviewPolyline2.getString("points");


            ArrayList<LatLng> route2 = decodePoly(encodedPolyline2);

            RouteResult routeResult = new RouteResult();
            routeResult.setRoute(route);
            routeResult.setRoute2(route2);
            routeResult.setDots(placeDots);
            return routeResult;
        } catch (Exception e) {
            e.printStackTrace();
            Log.e(MainActivity.TAG, ">>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<");
            Log.e(MainActivity.TAG, ">>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<");
            Log.e(MainActivity.TAG, ">>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<");
            Log.e(MainActivity.TAG, ">>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<");
            e.printStackTrace();
            Log.e(MainActivity.TAG, ">>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<");
            Log.e(MainActivity.TAG, ">>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<");
            Log.e(MainActivity.TAG, ">>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<");
            Log.e(MainActivity.TAG, ">>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<");
        }
        return null;
    }


    private ArrayList<LatLng> decodePoly(String encoded) {

        ArrayList<LatLng> poly = new ArrayList<LatLng>();
        int index = 0, len = encoded.length();
        int lat = 0, lng = 0;

        while (index < len) {
            int b, shift = 0, result = 0;
            do {
                b = encoded.charAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            int dlat = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
            lat += dlat;

            shift = 0;
            result = 0;
            do {
                b = encoded.charAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            int dlng = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
            lng += dlng;

            LatLng p = new LatLng((((double) lat / 1E5)),
                    (((double) lng / 1E5)));
            poly.add(p);
        }
        return poly;
    }

    public void setPointsInMap(LatLng origin) {
        if (httpResponse != null) {
            this.drawPoints(httpResponse);
        } else {
            HttpClient httpclient = new DefaultHttpClient();
            //http://pepo27devf.appspot.com/obtenerPuntos?latitudOrigen=19.42592174537003&longitudOrigen=-99.16573014110327
            HttpPost httppost = new HttpPost("http://pepo27devf.appspot.com/obtenerPuntos");
            try {
                List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();

                nameValuePairs.add(new BasicNameValuePair("latitudOrigen", "" + origin.latitude));
                nameValuePairs.add(new BasicNameValuePair("longitudOrigen", "" + origin.longitude));

                httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

                Log.e(MainActivity.TAG, "URL: " + httppost.getURI());

                // Execute HTTP Post Request
                HttpResponse response = httpclient.execute(httppost);

                String responseString = new BasicResponseHandler().handleResponse(response);

                Log.e(MainActivity.TAG, "JSON Result: " + responseString);
                this.drawPoints(responseString);

            } catch (Exception e) {
                e.printStackTrace();
            }
        }

    }

    public void setResponse(String respuesta) {
        this.httpResponse = respuesta;
    }

    public ArrayList<PlaceDot> drawPoints(String responseString) {
        try {
            JSONObject jsonRoute = new JSONObject(responseString);


            JSONArray keyPoints = jsonRoute.getJSONArray("puntosClave");

            ArrayList<PlaceDot> placeDots = new ArrayList<PlaceDot>();
            for (int i = 0; i < keyPoints.length(); i++) {

                JSONObject keyPoint = keyPoints.getJSONObject(i);

                double longitud = keyPoint.getDouble("longitud");
                double latitud = keyPoint.getDouble("latitud");
                int score = keyPoint.getInt("tipo");

                PlaceDot placeDot = new PlaceDot();
                placeDot.setScore(score);
                placeDot.setPlace(new LatLng(latitud, longitud));

                placeDots.add(placeDot);

            }
            return placeDots;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
