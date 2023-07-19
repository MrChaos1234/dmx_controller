import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.2
import QtQuick.Window 2.15

Item {
    id: selectedColorDisplay

    property var model: colorPickerQmlPresentationModel

    property real rPart: (model.r / 255.0)
    property real gPart: (model.g / 255.0)
    property real bPart: (model.b / 255.0)
    property real dimmer: (model.dimmer / 255.0)

    anchors.fill: parent

    Rectangle {
        id: colorDisplay
        anchors.fill: parent
                        color: Qt.rgba(rPart, gPart, bPart, dimmer)
    }
}
