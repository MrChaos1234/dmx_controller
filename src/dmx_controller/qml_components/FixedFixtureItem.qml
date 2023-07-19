import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."


Rectangle {
    id: fixedFixtureItem
    width: 54
    height: 54
    color: "white"

    property int fixture_id: 0
    property string image_source: "../data/fixture_library/symbols/none.png"
    property bool selected: false

    property real rPart: (colorPickerQmlPresentationModel.r / 255.0)
    property real gPart: (colorPickerQmlPresentationModel.g / 255.0)
    property real bPart: (colorPickerQmlPresentationModel.b / 255.0)
    property real dimmer: (colorPickerQmlPresentationModel.dimmer / 255.0)

    property real rPart_fixed: 0
    property real gPart_fixed: 0
    property real bPart_fixed: 0
    property real dimmer_fixed: 0

    Rectangle {
        id: itemBorder
        anchors.fill: parent
        z: 1
        color: "black"
    }
    Rectangle {
        id: itemBorderBlackBlock
        anchors.centerIn: parent
        width: 52
        height: 52
        z: 2
        color: "black"
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        drag.target: fixedFixtureItem

        onClicked: {
            console.log("clicked fixture " + fixture_id)
            if (selected) {
                // if the user deselects a fixture
                selected = false
                itemBorder.color = "black"
                stageViewQmlPresentationModel.remove_fixture_from_selection(fixture_id)
                // safe the choosen color and set the colorDisplay to the this color
                colorDisplay.opacity = 0
                rPart_fixed = rPart
                gPart_fixed = gPart
                bPart_fixed = bPart
                dimmer_fixed = dimmer
                colorDisplayFixedColor.opacity = 1
                // reset the colorPicker
                colorPickerQmlPresentationModel.r = 0
                colorPickerQmlPresentationModel.g = 0
                colorPickerQmlPresentationModel.b = 0
                // set the rotary encoders to zero -> hier noch Problem, da die werte zwar richtig angezeigt aber nicht aufs drehen wirksam werden
                doubleSpeedRotaryEncoderQmlPresentationModel0.position = 0
                doubleSpeedRotaryEncoderQmlPresentationModel1.position = 0
                doubleSpeedRotaryEncoderQmlPresentationModel2.position = 0
                doubleSpeedRotaryEncoderQmlPresentationModel3.position = 0
               
                // set the Fixture color selected color
                stageViewQmlPresentationModel.set_fixture_color(fixture_id, Math.round(rPart_fixed * 255), Math.round(gPart_fixed * 255), Math.round(bPart_fixed * 255), Math.round(dimmer_fixed * 255))
            
            } else {
                // If the user Selects a Fixture
                selected = true
                itemBorder.color = "red"
                stageViewQmlPresentationModel.add_fixture_to_selection(fixture_id)
                // make the fixed color invisible
                colorDisplayFixedColor.opacity = 0
                // set the colorPicker to the old color
                colorPickerQmlPresentationModel.r = Math.round(rPart_fixed * 255)
                colorPickerQmlPresentationModel.g = Math.round(gPart_fixed * 255)
                colorPickerQmlPresentationModel.b = Math.round(bPart_fixed * 255)
                colorPickerQmlPresentationModel.dimmer = Math.round(dimmer_fixed * 255)
                // set the rotary encoders to the old values -> hier noch Problem, da die werte zwar richtig angezeigt aber nicht aufs drehen wirksam werden
                doubleSpeedRotaryEncoderQmlPresentationModel0.position = Math.round(rPart_fixed * 255)
                doubleSpeedRotaryEncoderQmlPresentationModel1.position = Math.round(gPart_fixed * 255)
                doubleSpeedRotaryEncoderQmlPresentationModel2.position = Math.round(bPart_fixed * 255)
                doubleSpeedRotaryEncoderQmlPresentationModel3.position = Math.round(dimmer_fixed * 255)
                // make the colorDisplay visible
                colorDisplay.opacity = 1
            }   
        }
    } 

    // Image of the fixturetype
    Image {
        id: image
        anchors.top: parent.top
        anchors.topMargin: 1
        anchors.horizontalCenter: parent.horizontalCenter
        width: 36
        height: 36
        z: 4
        source: image_source
    } 

    // Text containing the fixture id
    Rectangle {
        id: fixtureIdBackground
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 1
        anchors.left: parent.left
        anchors.leftMargin: 1
        anchors.right: parent.right
        anchors.rightMargin: 1

        height: 15
        z: 4
        color: "black"

        Text {
            id: fixtureIdText
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            z: 4
            text: fixture_id
            font.family: "TW Cen MT"
            font.pixelSize: 10
            color: "white"
        }
    }
    

    // Color indicating the led color
    Rectangle {
        id: colorDisplay
        anchors.centerIn: parent
        width: 52
        height: 52

        opacity: 0

        z: 3

        color: Qt.rgba(rPart, gPart, bPart, dimmer)
    }

    Rectangle {
        id: colorDisplayFixedColor
        anchors.centerIn: parent
        width: 52
        height: 52

        opacity: 0

        z: 3

        color: Qt.rgba(rPart_fixed, gPart_fixed, bPart_fixed, dimmer_fixed)
    }
}
