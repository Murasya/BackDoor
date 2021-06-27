package com.example.backdoor

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Location
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.example.backdoor.databinding.ActivityMapsBinding
import com.google.android.gms.location.*
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.*
import com.google.android.gms.tasks.OnCompleteListener
import com.google.firebase.firestore.ktx.firestore
import com.google.firebase.firestore.ktx.toObject
import com.google.firebase.ktx.Firebase
import com.google.firebase.messaging.FirebaseMessaging
import com.google.firebase.storage.ktx.storage
import java.io.File
import java.util.*


class MapsActivity : AppCompatActivity(), OnMapReadyCallback, GoogleMap.OnPolylineClickListener,
    GoogleMap.OnPolygonClickListener {

    companion object {
        private const val PERMISSION_REQUEST_CODE = 1234
    }

    private lateinit var fusedLocationClient: FusedLocationProviderClient
    private lateinit var locationCallback: LocationCallback

    private lateinit var mMap: GoogleMap
    private lateinit var binding: ActivityMapsBinding
    private val db = Firebase.firestore
    //private var currentLocation = CurrentLocation()

    private var centerPosition = LatLng(0.0, 0.0);
    private var zoomMagnification = 0.0;
    private var zoomList = arrayOf(20,50,100,200,200,500,1000,2000,5000,10000,20000,50000,
                                100000,200000,200000,500000,1000000,2000000,5000000,10000000)

    private var current_location = LatLng(0.0, 0.0)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        FirebaseMessaging.getInstance().token.addOnCompleteListener(OnCompleteListener { task ->
            if (!task.isSuccessful) {
                Log.w("fcmToken", "Fetching FCM registration token failed", task.exception)
                return@OnCompleteListener
            }

            // Get new FCM registration token
            val token = task.result

            // Log and toast
            val msg = getString(R.string.msg_token_fmt) + token
            Log.d("fcmToken", msg)
            val user = User(msg)
            val userId = "AndroidUser"
            db.collection("Users").document(userId)
                .set(user)
                .addOnSuccessListener { Log.d("fcmToken", "DocumentSnapshot successfully written!") }
                .addOnFailureListener { e -> Log.w("fcmToken", "Error writing document", e) }
            val docRef = db.collection("CurrentLocation").document(userId)
            docRef.addSnapshotListener {snapshot, e ->
                if (e != null) {
                    Log.w("getFirebase", "listen:error", e)
                    return@addSnapshotListener
                }
                if(snapshot != null && snapshot.exists()) {
                    val currentLocation = snapshot.toObject<CurrentLocation>()!!
                    //if(currentLocation.latitude?.iterator() != null) {
                    Log.d("iscreateLocation", "true")
                    if(currentLocation.latitude != null && currentLocation.longitude != null) {
                        val points = ArrayList<LatLng>()
                        val lineOptions = PolylineOptions()
                        val latIterator = currentLocation.latitude.iterator()
                        val lonIterator = currentLocation.longitude.iterator()
                        while (latIterator.hasNext() && lonIterator.hasNext()) {
                            val lat = latIterator.next()
                            val lon = lonIterator.next()
                            points.add(LatLng(lat,lon))
                            Log.d("iscreateLocation", "lat : $lat, lon : $lon")
                            //Log.d("Polyline", "${mMap.}")
                        }
                        lineOptions.addAll(points);
                        lineOptions.width(10F);
                        lineOptions.color(0x550000ff);

                        calculationCenter(points)
                        mMap.addPolyline(lineOptions)
                    }
                    Log.d("getFirebase", "Current data: $currentLocation")
                } else {
                    Log.d("getFirebase", "Current data: null")
                }
            }
        })

        val storage = Firebase.storage
        var storageRef = storage.reference
        var pathReference = storageRef.child("IMG_0076.png")
        val localFile = File.createTempFile("images", "png")

        pathReference.getFile(localFile).addOnSuccessListener {
            Log.d("storage", "Local temp file has been created")
        }.addOnFailureListener {
            Log.d("storage", "Handle any errors")
        }

        requestPermission()

        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
        var updatedCount = 0
        locationCallback = object : LocationCallback() {
            override fun onLocationResult(locationResult: LocationResult?) {
                locationResult ?: return
                for (location in locationResult.locations){
                    updatedCount++
                    binding.locationText.text = "[${updatedCount}] ${location.latitude} , ${location.longitude}"
                    current_location = LatLng(location.latitude,location.longitude)
                }
            }
        }

        binding = ActivityMapsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        val mapFragment = supportFragmentManager
            .findFragmentById(R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this)

        binding.setCurrentLocation.setOnClickListener(object : View.OnClickListener {
            // クリック時に呼ばれるメソッド
            override fun onClick(view: View?) {
                mMap.moveCamera(CameraUpdateFactory.newLatLng(current_location))
            }
        })

        binding.setNavigation.setOnClickListener(object : View.OnClickListener {
            // クリック時に呼ばれるメソッド
            override fun onClick(view: View?) {
                mMap.moveCamera(CameraUpdateFactory.newLatLng(centerPosition))
                mMap.moveCamera(CameraUpdateFactory.zoomTo(zoomMagnification.toFloat()))
            }
        })
    }

    override fun onResume() {
        super.onResume()
        startLocationUpdates()
    }

    override fun onPause() {
        super.onPause()
        stopLocationUpdates()
    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    override fun onMapReady(googleMap: GoogleMap) {
        mMap = googleMap

        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return
        }
        mMap.setMyLocationEnabled(true);
        // Add a marker in Sydney and move the camera
        //val sydney = LatLng(-34.0, 151.0)
        //mMap.addMarker(MarkerOptions().position(sydney).title("Marker in Sydney"))
        //mMap.moveCamera(CameraUpdateFactory.newLatLng(sydney))
    }

    private fun startLocationUpdates() {
        val locationRequest = createLocationRequest() ?: return
        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return
        }
        fusedLocationClient.requestLocationUpdates(
            locationRequest,
            locationCallback,
            null)
    }

    private fun stopLocationUpdates() {
        fusedLocationClient.removeLocationUpdates(locationCallback)
    }

    private fun createLocationRequest(): LocationRequest? {
        return LocationRequest.create()?.apply {
            interval = 10000
            fastestInterval = 5000
            priority = LocationRequest.PRIORITY_HIGH_ACCURACY
        }
    }

    private fun sendLocationToGoogleMap() {
        // 起点の緯度経度
        val src_lat = current_location.latitude.toString()
        val src_ltg = current_location.longitude.toString()

        // 目的地の緯度経度
        val des_lat = "35.684752"
        val des_ltg = "139.707937"
        val intent = Intent()
        intent.action = Intent.ACTION_VIEW
        intent.setClassName(
            "com.google.android.apps.maps",
            "com.google.android.maps.MapsActivity"
        )

        // 起点の緯度,経度, 目的地の緯度,経度
        val str: String = java.lang.String.format(
            Locale.US,
            "http://maps.google.com/maps?saddr=%s,%s&daddr=%s,%s",
            src_lat, src_ltg, des_lat, des_ltg
        )
        intent.data = Uri.parse(str)
        startActivity(intent)
    }

    //盗まれた場合、自身の駐車場から盗難車の現在位置までの経路を生成
    private fun createLocationPAToStolenCar(googleMap: GoogleMap, currentLocation: CurrentLocation){
        var i = 0
        if(currentLocation.time?.iterator() != null) {
            while (currentLocation.time?.iterator()!!.hasNext()) {
                mMap.addPolyline(PolylineOptions()
                    .clickable(true)
                    .add(
                        currentLocation.latitude?.let { currentLocation.longitude?.let { it1 -> LatLng(it.get(i), it1.get(i)) } }))
                i = i+1
            }
        }
    // Store a data object with the polyline, used here to indicate an arbitrary type.
    }

    private fun calculationCenter(points : ArrayList<LatLng>){

        var latTmp = 0.0
        var lonTmp = 0.0

        var maxDistance = 0.0

        var zoomIdentifyNum = 0.0

        for (point in points) {
            latTmp = latTmp + point.latitude
            lonTmp = lonTmp + point.longitude
        }
        latTmp = latTmp/points.size
        lonTmp = lonTmp/points.size

        centerPosition = LatLng(latTmp,lonTmp)

        for (point in points) {
            if(maxDistance < centerPosition.distanceBetween(point))
                maxDistance = centerPosition.distanceBetween(point).toDouble()
        }

        for ((index,zoom) in (zoomList.withIndex())){
            if(zoom > maxDistance) {
                zoomMagnification = index.toDouble()
                if(index > 0 && index < zoomList.size)
                    zoomIdentifyNum = 1 - ((maxDistance - zoomList[index - 1]) / (zoom - zoomList[index - 1]))
                Log.d("zoomTask", "zoom : $zoom, maxDistace : $maxDistance, zoomMagnification : $zoomMagnification, zoomIdentifyNum : $zoomIdentifyNum")
                break
            }
        }
        zoomMagnification = zoomList.size - zoomMagnification + 1 + zoomIdentifyNum
    }

    fun LatLng.distanceBetween(toLatLng: LatLng): Float {
        val results = FloatArray(1)
        try {
            Location.distanceBetween(
                this.latitude, this.longitude,
                toLatLng.latitude, toLatLng.longitude,
                results
            )
        } catch (e: IllegalArgumentException) {
            return -1.0f
        }
        return results[0]
    }

    private fun requestPermission() {
        val permissionAccessCoarseLocationApproved =
            ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) ==
                    PackageManager.PERMISSION_GRANTED &&
                    ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) ==
                    PackageManager.PERMISSION_GRANTED

        if (permissionAccessCoarseLocationApproved) {
            val backgroundLocationPermissionApproved = ActivityCompat
                .checkSelfPermission(this, Manifest.permission.ACCESS_BACKGROUND_LOCATION) ==
                    PackageManager.PERMISSION_GRANTED

            if (backgroundLocationPermissionApproved) {
                // フォアグラウンドとバックグランドのバーミッションがある
            } else {
                // フォアグラウンドのみOKなので、バックグラウンドの許可を求める
                ActivityCompat.requestPermissions(this,
                    arrayOf(Manifest.permission.ACCESS_BACKGROUND_LOCATION),
                    PERMISSION_REQUEST_CODE
                )
            }
        } else {
            // 位置情報の権限が無いため、許可を求める
            ActivityCompat.requestPermissions(this,
                arrayOf(
                    Manifest.permission.ACCESS_COARSE_LOCATION,
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_BACKGROUND_LOCATION
                ),
                PERMISSION_REQUEST_CODE
            )
        }
    }

    override fun onPolylineClick(p0: Polyline) {
        TODO("Not yet implemented")
    }

    override fun onPolygonClick(p0: Polygon) {
        TODO("Not yet implemented")
    }

}