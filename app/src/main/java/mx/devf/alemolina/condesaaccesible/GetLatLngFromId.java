package mx.devf.alemolina.condesaaccesible;

import android.os.AsyncTask;
import android.util.Log;

import com.google.android.gms.maps.model.LatLng;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * Created by alemolina on 7/18/14.
 */
public class GetLatLngFromId  extends AsyncTask<String, Void, LatLng> {

    protected interface OnLatLngListener {
        public void latLngReady(LatLng latlng);
    }


    protected static final String TYPE_DETAILS = "/details";
    private OnLatLngListener listener;


    public void setListener(OnLatLngListener listener) {
        this.listener = listener;
    }


    // https://maps.googleapis.com/maps/api/place/details/json/?key=AIzaSyBVy5AeNC0FzQD1aKpZciL06wtLQ5qd2k4&place_id=ChIJhZD8llz_0YURsKigpkDsai8
    public LatLng getLatLngFromId(String id){

        LatLng latlng = null;

        HttpURLConnection conn = null;
        StringBuilder jsonResults = new StringBuilder();
        try {
            StringBuilder sb = new StringBuilder(PlacesAutoComplete.PLACES_API_BASE + TYPE_DETAILS + PlacesAutoComplete.OUT_JSON);

            sb.append("?placeid=" + id.toString());
            sb.append("&key=" + PlacesAutoComplete.API_KEY);

            URL url = new URL(sb.toString());
            conn = (HttpURLConnection) url.openConnection();
            InputStreamReader in = new InputStreamReader(conn.getInputStream());

            // Load the results into a StringBuilder
            int read;
            char[] buff = new char[1024];
            while ((read = in.read(buff)) != -1) {
                jsonResults.append(buff, 0, read);
            }
        } catch (MalformedURLException e) {
            Log.e(PlacesAutoComplete.LOG_TAG, "Error processing Places API URL", e);
            return latlng;
        } catch (IOException e) {
            Log.e(PlacesAutoComplete.LOG_TAG, "Error connecting to Places API", e);
            return latlng;
        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }

        try {
            Log.i(PlacesAutoComplete.LOG_TAG, jsonResults.toString());
            // Create a JSON object hierarchy from the results
            JSONObject jsonObj = new JSONObject(jsonResults.toString());
            JSONObject result = jsonObj.getJSONObject("result");
            JSONObject geometry = result.getJSONObject("geometry");
            JSONObject location = geometry.getJSONObject("location");
            double lat = location.getDouble("lat");
            double lng = location.getDouble("lng");
            latlng = new LatLng(lat, lng);


        } catch (JSONException e) {
            Log.e(PlacesAutoComplete.LOG_TAG, "Cannot process JSON results", e);
        }

        return latlng;
    }

    @Override
    protected LatLng doInBackground(String... params) {
        return getLatLngFromId(params[0]);
    }
    @Override
    protected void onPostExecute(LatLng position) {
        listener.latLngReady(position);
    }

}
