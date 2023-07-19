import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../qml_components"

Item {
    id: setupPage
    anchors.fill: parent
    Rectangle {
        id: setupPageRect
        anchors.fill: parent
        color: "#121212"

        Text {
            id: text
            anchors.centerIn: parent
            text: "Setup Page Placeholder"
            font.pixelSize: 30
            color: "#ffffff"
        }

        DmxFixturePatch {
            id: dmxFixturePatchView
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.top: parent.top
        }

        StageSetupView {
            id: stageSetupView
            anchors.left: dmxFixturePatchView.right
        }
    }
}

