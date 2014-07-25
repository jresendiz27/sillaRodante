package mx.devf.alemolina.condesaaccesible;

import android.content.Context;
import android.graphics.Color;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AutoCompleteTextView;
import android.widget.Button;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptor;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;

import java.util.ArrayList;


public class MainActivity extends FragmentActivity {

    private GoogleMap mMap; // Might be null if Google Play services APK is not available.

    // Definition of the buttons, which will be used in various functions
    private Button buttonGreen;
    private Button buttonBlue;
    private Button buttonYellow;
    private Button buttonRed;

    private View.OnClickListener buttonListener;

    public static final String TAG = "CondesaAccesible";

    // Definition of "latlng" which will contain current location information.
    private LatLng latlng;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setUpMapIfNeeded();

        // We link our button objects with the Views in the xml
        buttonGreen = (Button) findViewById(R.id.buttonGreen);
        buttonBlue = (Button) findViewById(R.id.buttonBlue);
        buttonYellow = (Button) findViewById(R.id.buttonYellow);
        buttonRed = (Button) findViewById(R.id.buttonRed);

        // The button listener states that, on click, the function dropColorPin will be called
        buttonListener = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                dropColorPin((Button) v);
            }
        };

        // we call the function buttonListener
        buttonGreen.setOnClickListener(buttonListener);
        buttonBlue.setOnClickListener(buttonListener);
        buttonYellow.setOnClickListener(buttonListener);
        buttonRed.setOnClickListener(buttonListener);


        AutoCompleteTextView autoCompView = (AutoCompleteTextView) findViewById(R.id.autocompleteView);
        final PlacesAutoCompleteAdapter adapter = new PlacesAutoCompleteAdapter(this, R.layout.list_item);
        autoCompView.setAdapter(adapter);

        AdapterView.OnItemClickListener itemClickListener = new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                String placeId = adapter.getItemPlaceId(position);
                final String placeName = adapter.getItem(position);
                GetLatLngFromId latlngService = new GetLatLngFromId();
                latlngService.setListener(new GetLatLngFromId.OnLatLngListener() {
                    @Override
                    public void latLngReady(LatLng destination) {
                       setDestinationPin(destination, placeName);
                       drawPath(latlng, destination);
                    }
                });
                latlngService.execute(placeId);
            }
        };
        autoCompView.setOnItemClickListener(itemClickListener);


        Log.i(TAG, "ADIOS");
    }

    private void setDestinationPin(LatLng latlng, String placeName) {
        //Log.i(TAG, latlng.toString());
        mMap.animateCamera(CameraUpdateFactory.newLatLng(latlng));
        mMap.addMarker(new MarkerOptions().position(latlng).title(placeName).icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE)));
    }

    private void drawPath(LatLng origin, LatLng destination){
        GetPointsInRoute pointService = new GetPointsInRoute();
        pointService.setListener(new GetPointsInRoute.OnPathListener() {
            @Override
            public void latLngReady(RouteResult routeResult) {

                drawRoute(routeResult.getRoute());
                drawDots(routeResult.getDots());

            }
        });
        pointService.execute(origin, destination);
    }

    private void drawDots(ArrayList<PlaceDot> dots) {
        for (int i=0; i<dots.size(); i++){
            PlaceDot placeDot = dots.get(i);
            String title;
            BitmapDescriptor hue;

            if (4 == placeDot.getScore()) {
                title = "Rampa";
                hue = BitmapDescriptorFactory.fromResource(R.drawable.dot_green);
            } else if (3 == placeDot.getScore()) {
                title = "Camino";
                hue = BitmapDescriptorFactory.fromResource(R.drawable.dot_blue);
            } else if (2 == placeDot.getScore()) {
                title = "Alerta";
                hue = BitmapDescriptorFactory.fromResource(R.drawable.dot_yellow);
            } else {
                title = "Impasable";
                hue = BitmapDescriptorFactory.fromResource(R.drawable.dot_red);
            }
            // Drops a marker in the current location.
            mMap.addMarker(new MarkerOptions().position(placeDot.getPlace()).title(title).icon(hue).anchor(0.5f,0.5f));
        }
    }

    private void drawRoute(ArrayList<LatLng> route) {

        PolylineOptions polyLineOptions = new PolylineOptions();
        polyLineOptions.addAll(route);
        polyLineOptions.width(5);
        polyLineOptions.color(Color.BLUE);
        mMap.addPolyline(polyLineOptions);

    }

    @Override
    protected void onResume() {
        super.onResume();
        setUpMapIfNeeded();
    }

    // guess what dropColorPin does? You guessed right! (I DO hope so at least) drops a pin, the color will vary depending on the button that was clicked.
    private void dropColorPin(Button button) {
        String title;
        BitmapDescriptor hue;
        int score;
        if (button.equals(buttonGreen)) {
            title = "Rampa";
            //hue = BitmapDescriptorFactory.fromResource(R.drawable.dot_green);
            hue = BitmapDescriptorFactory.fromResource(R.drawable.dot_green);
            score = 4;
        } else if (button.equals(buttonBlue)) {
            title = "Camino";
            hue = BitmapDescriptorFactory.fromResource(R.drawable.dot_blue);
            score = 3;
        } else if (button.equals(buttonYellow)) {
            title = "Alerta";
            hue = BitmapDescriptorFactory.fromResource(R.drawable.dot_yellow);
            score = 2;
        } else {
            title = "Impasable";
            hue = BitmapDescriptorFactory.fromResource(R.drawable.dot_red);
            score = 1;
        }
        // Drops a marker in the current location.
        mMap.addMarker(new MarkerOptions().position(latlng).title(title).icon(hue).anchor(0.5f,0.5f));
        // Send score to backend
        sendScore(score, latlng);
    }

    /**
     * Sets up the map if it is possible to do so (i.e., the Google Play services APK is correctly
     * installed) and the map has not already been instantiated.. This will ensure that we only ever
     * call {@link #setUpMap()} once when {@link #mMap} is not null.
     * <p/>
     * If it isn't installed {@link SupportMapFragment} (and
     * {@link com.google.android.gms.maps.MapView MapView}) will show a prompt for the user to
     * install/update the Google Play services APK on their device.
     * <p/>
     * A user can return to this FragmentActivity after following the prompt and correctly
     * installing/updating/enabling the Google Play services. Since the FragmentActivity may not
     * have been completely destroyed during this process (it is likely that it would only be
     * stopped or paused), {@link #onCreate(Bundle)} may not be called again so we should call this
     * method in {@link #onResume()} to guarantee that it will be called.
     */
    private void setUpMapIfNeeded() {
        // Do a null check to confirm that we have not already instantiated the map.
        if (mMap == null) {
            // Try to obtain the map from the SupportMapFragment.
            mMap = ((SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map))
                    .getMap();
            // Check if we were successful in obtaining the map.
            if (mMap != null) {
                setUpMap();
            }
        }
    }

    /**
     * This is where we can add markers or lines, add listeners or move the camera. In this case, we
     * just add a marker near Africa.
     * <p/>
     * This should only be called once and when we are sure that {@link #mMap} is not null.
     */
    private void setUpMap() {
        mMap.moveCamera(CameraUpdateFactory.zoomTo(16));
        mMap.setMyLocationEnabled(true);

        LocationManager locationManager = (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);

        // Define a listener that responds to location updates
        LocationListener locationListener = new LocationListener() {
            public void onLocationChanged(Location location) {
                // Called when a new location is found by the network location provider.
                makeUseOfNewLocation(location);
            }

            public void onStatusChanged(String provider, int status, Bundle extras) {
            }

            public void onProviderEnabled(String provider) {
            }

            public void onProviderDisabled(String provider) {
            }
        };

        // Register the listener with the Location Manager to receive location updates
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, locationListener);
        locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 0, 0, locationListener);



    }

    private void makeUseOfNewLocation(Location location) {
        boolean shouldMoveMap = latlng == null;
        latlng = new LatLng(location.getLatitude(), location.getLongitude());
        if(shouldMoveMap){
            mMap.addMarker(new MarkerOptions().position(latlng).title("Aqui estas"));
            mMap.moveCamera(CameraUpdateFactory.newLatLng(latlng));
        }
    }

    ///////////////////////envio de datos
    public void sendScore(int score, LatLng latlng) {
        try {
            HTTPTask task = new HTTPTask();
            task.setApplicationContext(getApplicationContext());
            task.execute("" + latlng.latitude, "" + latlng.longitude, "" + score);
        } catch (Exception e) {
            Log.e(TAG, "error");
            e.printStackTrace();
        }
    }

}
