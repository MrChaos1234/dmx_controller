import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.2

Item {
    id: stageView
    property var qml_presentation_model: None

    width: 1100
    height: 800

    Rectangle {
        id: stageViewBackground
        anchors.fill: parent
        color: "black"
    }
   
    Rectangle {
        id: stageViewMainField
        width: 1000
        height: 560
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 50
        color: "gray"
    }

    // Dynamicaly Create dragable rectangles

    // Temp test model
    ListModel {
        id: listModel
        ListElement {
            pos_x: 100
            pos_y: 100
        }
        ListElement {
            pos_x: 300
            pos_y: 300
        }
    }

}


