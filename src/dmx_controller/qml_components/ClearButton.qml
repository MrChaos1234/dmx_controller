import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."


Rectangle {
    id: clearButton
    width: 70
    height: 70
    color: "black"
    z: 1
    
    MouseArea {
        id: mouseAreaAddCue
        anchors.fill: parent
    
        onClicked: {
            console.log("clear button clicked")
            artnetOutputQmlPresentationModel.clear_output()
        }
    } 
    
    // Text 
    Rectangle {
        id: background
        anchors.centerIn: parent
        color: "#2b2b2b"
        width: 66
        height: 66
        z: 2

        Text {
            id: text
            anchors.centerIn: parent
            text: "Clear"
            font.family: "TW Cen MT"
            font.pixelSize: 10
            color: "white"
            z:3
        }
    }
}
