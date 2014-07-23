package mx.devf.alemolina.condesaaccesible;

import android.os.AsyncTask;
import android.util.Log;

import com.google.android.gms.maps.model.LatLng;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by alemolina on 7/22/14.
 */
public class GetPointsInRoute extends AsyncTask<LatLng, Integer, ArrayList<LatLng>> {

    protected interface OnPathListener {
        public void latLngReady(ArrayList<LatLng> latlng);
    }

    private OnPathListener listener;

    public void setListener(OnPathListener listener) {
        this.listener = listener;
    }

    @Override
    protected ArrayList<LatLng> doInBackground(LatLng... latlngs) {
        return postData(latlngs[0], latlngs[1]);
    }

    protected void onPostExecute(ArrayList<LatLng> result) {
        listener.latLngReady(result);
    }

    protected void onProgressUpdate(Integer... progress) {
        //pb.setProgress(progress[0]);
    }

    public ArrayList<LatLng> postData(LatLng origin, LatLng destination) {
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

            Log.i(MainActivity.TAG, "URL: "+httppost.getURI());

            // Execute HTTP Post Request
            HttpResponse response = httpclient.execute(httppost);

            String responseString = new BasicResponseHandler().handleResponse(response);

            Log.i(MainActivity.TAG, "JSON Result: "+responseString);

            JSONObject jsonRoute = new JSONObject(responseString);
            JSONObject possibleRoutes = jsonRoute.getJSONObject("rutasPosibles");
            JSONArray routes = possibleRoutes.getJSONArray("routes");
            JSONObject firstRoute = routes.getJSONObject(0);
            JSONObject overviewPolyline = firstRoute.getJSONObject("overview_polyline");
            String encodedPolyline = overviewPolyline.getString("points");

            return decodePoly(encodedPolyline);


        } catch (ClientProtocolException e) {
            // TODO Auto-generated catch block
        } catch (IOException e) {
            // TODO Auto-generated catch block
        } catch (JSONException e) {
            e.printStackTrace();
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
}
