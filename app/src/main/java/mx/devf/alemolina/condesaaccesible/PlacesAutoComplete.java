package mx.devf.alemolina.condesaaccesible;

import android.os.AsyncTask;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;

/**
 * Created by alemolina on 7/16/14.
 */
public class PlacesAutoComplete extends AsyncTask<String, Void, ArrayList<String>> {
    protected static final String LOG_TAG = "CondesaAccesible";

    protected static final String PLACES_API_BASE = "https://maps.googleapis.com/maps/api/place";
    protected static final String TYPE_AUTOCOMPLETE = "/autocomplete";

    protected static final String OUT_JSON = "/json";

    protected static final String API_KEY = "AIzaSyBVy5AeNC0FzQD1aKpZciL06wtLQ5qd2k4";

    @Override
    protected ArrayList<String> doInBackground(String... params) {
        return autocomplete(params[0]);
    }

    private ArrayList<String> idList = null;
    private ArrayList<String> suggestions = null;

    public String getItemPlaceId(int position){
        return idList.get(position);
    }


    public ArrayList<String> autocomplete(String input) {

        HttpURLConnection conn = null;
        StringBuilder jsonResults = new StringBuilder();
        try {
            StringBuilder sb = new StringBuilder(PLACES_API_BASE + TYPE_AUTOCOMPLETE + OUT_JSON);
            sb.append("?key=" + API_KEY);
            sb.append("&components=country:mx");
            sb.append("&input=" + URLEncoder.encode(input, "utf8"));

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
            Log.e(LOG_TAG, "Error processing Places API URL", e);
            return suggestions;
        } catch (IOException e) {
            Log.e(LOG_TAG, "Error connecting to Places API", e);
            return suggestions;
        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }

        try {
            // Log.i(LOG_TAG, jsonResults.toString());
            // Create a JSON object hierarchy from the results
            JSONObject jsonObj = new JSONObject(jsonResults.toString());
            JSONArray predsJsonArray = jsonObj.getJSONArray("predictions");

            // Extract the Place descriptions from the results
            idList = new ArrayList<String>(predsJsonArray.length());
            for (int i = 0; i < predsJsonArray.length(); i++) {
                idList.add(predsJsonArray.getJSONObject(i).getString("place_id"));
            }

            suggestions = new ArrayList<String>(predsJsonArray.length());
            for (int i = 0; i < predsJsonArray.length(); i++) {
                suggestions.add(predsJsonArray.getJSONObject(i).getString("description"));
            }

        } catch (JSONException e) {
            Log.e(LOG_TAG, "Cannot process JSON results", e);
        }

        return suggestions;
    }

}
