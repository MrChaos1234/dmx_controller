import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../qml_components"

Item {
    id: recordPage
    anchors.fill: parent
    Rectangle {
        id: s
        anchors.fill: parent
        color: "#121212"

        StageSelectingView {
            id: stageSelectingView
            anchors.left: parent.left
            width:1050
        }

        CueList {
            id: cueList
            anchors.left: stageSelectingView.right
            anchors.leftMargin: 10
            anchors.top: parent.top
            
        }
    }
}

