// Auto-generated. Do not edit!

// (in-package mbed_interface.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class JointAngles {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.joints = null;
    }
    else {
      if (initObj.hasOwnProperty('joints')) {
        this.joints = initObj.joints
      }
      else {
        this.joints = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type JointAngles
    // Serialize message field [joints]
    bufferOffset = _arraySerializer.float32(obj.joints, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type JointAngles
    let len;
    let data = new JointAngles(null);
    // Deserialize message field [joints]
    data.joints = _arrayDeserializer.float32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 4 * object.joints.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'mbed_interface/JointAngles';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e2a0e438b445b98def0f0ba6a2a85f58';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32[] joints
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new JointAngles(null);
    if (msg.joints !== undefined) {
      resolved.joints = msg.joints;
    }
    else {
      resolved.joints = []
    }

    return resolved;
    }
};

module.exports = JointAngles;
