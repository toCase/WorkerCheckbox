import QtQuick 6.5
import QtQuick.Controls 6.5
import QtQuick.Controls.Fusion
import QtQuick.Layouts
import QtQuick.Dialogs

Item {

    function load(){
        model_ttn.loadModel()
        // thread.start()
    }


    QtObject {
        id: internal

        property string id: "0"

        function selectRow(i){
            timerOff()

            table.currentIndex = i
            id = model_ttn.getData(i, "id")
        }

        function deleteRow(){
            timerOff()

            if (id !== "0"){
                model_ttn.deleteTTN(id)
            }
        }

        function deleteDone(){
            timerOff()

            model_ttn.deleteDone()

        }

        function updateNova(){
            timerOff()
            tNova.start()
        }
    }

    Connections {
        target: tNova
        function onStarted(){
            progress.visible = true
            progress.value = 0
            but_update.enabled = false
        }
        function onWorking(val){
            progress.value = val
        }
        function onFinished(){
            progress.visible = false
            progress.value = 0
            but_update.enabled = true
            model_ttn.loadModel()
        }
        function onFail(message){
            progress.visible = false
            progress.value = 0
            but_update.enabled = true
        }

    }


    ColumnLayout {
        id: columnLayout
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        spacing: 10

        RowLayout {
            id: rowLayout
            Layout.fillWidth: true
            Layout.maximumHeight: 35
            Layout.minimumHeight: 35

            Button {
                id: but_del
                Layout.maximumWidth: 100
                Layout.minimumWidth: 100
                Layout.fillHeight: true
                text: qsTr("Видалити")
                onClicked: internal.deleteRow()
            }
            Button {
                id: but_del_done
                Layout.maximumWidth: implicitWidth
                Layout.minimumWidth: implicitWidth
                Layout.fillHeight: true
                text: qsTr("Видалити всі оброблені")
                onClicked: internal.deleteDone()
            }

            Item{
                Layout.fillWidth: true
                visible: !progress.visible
            }

            ProgressBar {
                id: progress
                Layout.fillWidth: true
                Layout.minimumHeight: 5
                Layout.maximumHeight: 5
                visible: false
                value: 0
            }

            Button {
                id: but_update
                Layout.maximumWidth: implicitWidth
                Layout.minimumWidth: implicitWidth
                Layout.fillHeight: true
                text: qsTr("Перевірити статуси ТТН Нової Пошти")
                onClicked: internal.updateNova()
            }

        }


        ListView {
            id: table
            Layout.fillHeight: true
            Layout.fillWidth: true
            model: model_ttn
            clip: true
            // delegate: rowDelegate
            delegate: Item {

                width: table.width
                implicitHeight: itemCol.implicitHeight


                ColumnLayout{
                    id: itemCol
                    anchors.fill: parent

                    RowLayout {
                        Layout.fillWidth: true
                        Layout.minimumHeight: 35
                        Layout.maximumHeight: 35
                        spacing: 10

                        Label {
                            Layout.minimumWidth: 60
                            Layout.maximumWidth: 60
                            Layout.leftMargin: 10
                            text: num
                            font.pointSize: 11
                            font.bold: true
                            horizontalAlignment: Qt.AlignLeft
                            verticalAlignment: Qt.AlignVCenter
                        }

                        Label {
                            Layout.minimumWidth: 200
                            Layout.maximumWidth: 200
                            text: phone
                            font.pointSize: 11
                            font.bold: true
                            horizontalAlignment: Qt.AlignLeft
                            verticalAlignment: Qt.AlignVCenter

                        }
                        Label {
                            Layout.minimumWidth: 200
                            Layout.maximumWidth: 200
                            text: num_ttn
                            font.pointSize: 11
                            font.bold: true
                            horizontalAlignment: Qt.AlignRight
                            verticalAlignment: Qt.AlignVCenter
                        }

                        Label {
                            Layout.fillWidth: true
                            text: statusNP
                            // wrapMode: Text.WordWrap
                            clip: true
                            font.pointSize: 9
                            horizontalAlignment: Qt.AlignLeft
                            verticalAlignment: Qt.AlignVCenter
                        }
                        Label {
                            Layout.minimumWidth: 80
                            Layout.maximumWidth: 80
                            Layout.leftMargin: 10
                            text: statusCB
                            color: clr
                            font.pointSize: 11
                            font.bold: true
                            horizontalAlignment: Qt.AlignRight
                            verticalAlignment: Qt.AlignVCenter
                        }
                        Label {
                            Layout.minimumWidth: 150
                            Layout.maximumWidth: 150
                            Layout.rightMargin: 30
                            text: dateCB
                            font.pointSize: 9
                            horizontalAlignment: Qt.AlignRight
                            verticalAlignment: Qt.AlignVCenter
                        }
                    }

                    Repeater {
                        Layout.fillWidth: true
                        implicitHeight: detailEl.implicitHeight
                        model: base.detail_getX(id)

                        Text {
                            id: detailEl
                            leftPadding: 50
                            bottomPadding: 5
                            height: 20

                            required property string modelData
                            text: modelData
                            font.pointSize: 9
                            font.italic: true
                        }
                    }


                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: internal.selectRow(index)
                }
            }

            highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
            focus: true
        }
    }


    Connections {
        target: thread
        function onWorking(val){
            progress.value = val
        }
    }


}
