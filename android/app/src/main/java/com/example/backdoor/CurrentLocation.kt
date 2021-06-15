package com.example.backdoor

import com.google.firebase.Timestamp

data class CurrentLocation(
    val latitude: List<Double>? = null,
    val longitude: List<Double>? = null,
    val time: List<Timestamp>? = null,
)
