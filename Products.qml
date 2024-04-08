import QtQuick 6.5
import QtQuick.Controls 6.5
import QtQuick.Controls.Fusion
import QtQuick.Layouts

Item {


    function load() {
        modelProduct.loadModel()
    }

    QtObject {
        id: internal

        function update_product(){
            timerOff()

            tGoods.start()
        }
    }

    Connections {
        target: tGoods

        function onStarted(){
            progress.visible = true
            but_update.enabled = false
        }

        function onWorking(val){
            progress.value = val
        }

        function onFinished(){
            progress.visible = false
            progress.value = 0
            modelProduct.loadModel()
            but_update.enabled = true
        }

        function onFail(message){
            progress.visible = false
            progress.value = 0
            err.visible = true
            err.text = message
            but_update.enabled = true
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 15

        RowLayout {
            Layout.fillWidth: true
            Layout.minimumHeight: 30
            Layout.maximumHeight: 30

            spacing: 15

            Label {
                visible: false
                Layout.fillHeight: true
                Layout.minimumWidth: 150
                Layout.maximumWidth: 150
                font.pointSize: 13
                text: qsTr("Товари в Checkbox")
                verticalAlignment: Qt.AlignVCenter
            }
            Item {
                visible: !progress.visible
                Layout.fillWidth: true
            }

            Label {
                id: err
                visible: false
                Layout.fillHeight: true
                Layout.fillWidth: true
                font.pointSize: 9
                verticalAlignment: Qt.AlignVCenter
            }
            ProgressBar {
                id: progress
                visible: false
                Layout.fillWidth: true
                Layout.minimumHeight: 5
                Layout.maximumHeight: 5
                value: 0
            }
            Button {
                id: but_update
                Layout.fillHeight: true
                Layout.minimumWidth: 120
                Layout.maximumWidth: 120
                text: qsTr("Оновити")

                onClicked: internal.update_product()
            }
        }

        ListView {
            id: table
            Layout.fillHeight: true
            Layout.fillWidth: true
            model: modelProduct
            clip: true
            delegate: Item {
                width: table.width
                height: 35
                RowLayout {
                    anchors.fill: parent
                    Layout.minimumHeight: 30
                    Layout.maximumHeight: 30
                    spacing: 10

                    Label {
                        visible: false
                        Layout.minimumWidth: 80
                        Layout.maximumWidth: 80
                        text: id
                    }

                    Label {
                        Layout.minimumWidth: 240
                        Layout.maximumWidth: 240
                        Layout.leftMargin: 10
                        text: p_ids
                        font.pointSize: 9
                        horizontalAlignment: Qt.AlignLeft
                        verticalAlignment: Qt.AlignVCenter
                    }
                    Label {
                        Layout.minimumWidth: 60
                        Layout.maximumWidth: 60
                        text: p_code
                        font.pointSize: 11
                        horizontalAlignment: Qt.AlignLeft
                        verticalAlignment: Qt.AlignVCenter
                    }
                    Label {
                        Layout.fillWidth: true
                        text: p_name
                        font.pointSize: 11
                        horizontalAlignment: Qt.AlignLeft
                        verticalAlignment: Qt.AlignVCenter
                    }
                    Label {
                        Layout.minimumWidth: 60
                        Layout.maximumWidth: 60
                        Layout.rightMargin: 30
                        text: p_price / 100
                        font.pointSize: 9
                        horizontalAlignment: Qt.AlignRight
                        verticalAlignment: Qt.AlignVCenter
                    }
                }
            }
        }
    }
}
