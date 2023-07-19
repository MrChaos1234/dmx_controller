import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "qml_components"
import "qml_pages"

Window {
    visible: true
    visibility: Window.FullScreen

    property bool live_page_loaded: false
    property bool setup_page_loaded: false
    property bool record_page_loaded: false

    Item {
        id: root
        anchors.fill: parent

        // Bckground
        Rectangle {
            id: mainBackground
            anchors.fill: parent

            Image {
                anchors.fill: parent
                source: "res/Background.png"
                fillMode: Image.PreserveAspectCrop
            }
        }

        // Loader with the main pages
        Loader {
            id: mainLoader
            anchors {
                top: parent.top
                left: parent.left
                leftMargin: 105
                right: parent.right
                rightMargin: 105
                bottom: hardwareIndicatorRotaryEncoder.top
                bottomMargin: 8
            }
            source: "qml_pages/LivePage.qml"
            //source: "qml_pages/RecordPage.qml"  // this one default for now

            onLoaded: {
                console.log("Loaded: " + source)
                if (source == "file:///home/pi/Desktop/dmx_controller/src/dmx_controller/qml_pages/RecordPage.qml") {
                    live_page_loaded = false
                    setup_page_loaded = false
                    record_page_loaded = true
                    console.log("Record page loaded")
                } else if (source == "file:///home/pi/Desktop/dmx_controller/src/dmx_controller/qml_pages/SetupPage.qml") {
                    live_page_loaded = false
                    setup_page_loaded = true
                    record_page_loaded = false
                } else if (source == "file:///home/pi/Desktop/dmx_controller/src/dmx_controller/qml_pages/LivePage.qml") {
                    live_page_loaded = true
                    setup_page_loaded = false
                    record_page_loaded = false
                }
            }
        }

        // Right Menu Bar to switch between pages
        RightMenuBar {
            id: rightMenuBar
        }

        // Rotary encoders bottom bar
        Item {
            id: hardwareIndicatorRotaryEncoder
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 2
            anchors.left: parent.left
            anchors.leftMargin: 1031
            width: rotaryEncoderRow.width
            height: 125

            visible: record_page_loaded ? true : false  // only visible on record page

            SelectedColorDisplay {
                id: selectedColorDisplay
                anchors {
                    top: parent.top
                    topMargin: 2
                    bottom: rotaryEncoderRow.top
                    bottomMargin: 2
                    left: rotaryEncoderRow.left
                    right: parent.right
                } 
            }

            Row {
                id: rotaryEncoderRow
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                spacing: 0

                DoubleSpeedRotaryEncoder {
                    id: doubleSpeedRotaryEncoder0
                    model: doubleSpeedRotaryEncoderQmlPresentationModel0
                    purpose: "RED"
                }
                DoubleSpeedRotaryEncoder {
                    id: doubleSpeedRotaryEncoder1
                    model: doubleSpeedRotaryEncoderQmlPresentationModel1
                    purpose: "GREEN"
                }
                DoubleSpeedRotaryEncoder {
                    id: doubleSpeedRotaryEncoder2
                    model: doubleSpeedRotaryEncoderQmlPresentationModel2
                    purpose: "BLUE"
                }
                DoubleSpeedRotaryEncoder {
                    id: doubleSpeedRotaryEncoder3
                    model: doubleSpeedRotaryEncoderQmlPresentationModel3
                    purpose: "DIMMER"
                }
            }
        }

        // Bottom bar
        // Image{
        //     visible: record_page_loaded ? true : false ||  live_page_loaded ? true : false // only visible on record page and live page
        //     id: dummyL
        //     anchors.bottom: parent.bottom
        //     anchors.left: parent.left
            
        //     source: "res/dummy_l.png"
        // }

        Faders {
            visible: live_page_loaded ? true : false // only visible on live page
            id: faders
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.leftMargin: 105
            width: 400
            height: 125

        }


        Image{
            visible: record_page_loaded ? true : false ||  live_page_loaded ? true : false // only visible on record page and live page
            id: dummyR
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            
            source: "res/dummy_r.png"
        }

        // DMX List in bottom bar
        DmxList {
            visible: setup_page_loaded ? true : false // only visible on setup page
            id: dmxList
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 3
            anchors.left: parent.left
            anchors.leftMargin: 105
            anchors.right: parent.right
            anchors.rightMargin: 105
            height: 120
        }
    }
}
