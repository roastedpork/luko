// Auto-generated. Do not edit!

// (in-package led_driver.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class LightDriver {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.op = null;
      this.image = null;
    }
    else {
      if (initObj.hasOwnProperty('op')) {
        this.op = initObj.op
      }
      else {
        this.op = '';
      }
      if (initObj.hasOwnProperty('image')) {
        this.image = initObj.image
      }
      else {
        this.image = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type LightDriver
    // Serialize message field [op]
    bufferOffset = _serializer.string(obj.op, buffer, bufferOffset);
    // Serialize message field [image]
    bufferOffset = _arraySerializer.uint32(obj.image, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type LightDriver
    let len;
    let data = new LightDriver(null);
    // Deserialize message field [op]
    data.op = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [image]
    data.image = _arrayDeserializer.uint32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.op.length;
    length += 4 * object.image.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'led_driver/LightDriver';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '94104f9d0ed4c5d119270c5f8f23d22b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string op
    uint32[] image
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new LightDriver(null);
    if (msg.op !== undefined) {
      resolved.op = msg.op;
    }
    else {
      resolved.op = ''
    }

    if (msg.image !== undefined) {
      resolved.image = msg.image;
    }
    else {
      resolved.image = []
    }

    return resolved;
    }
};

module.exports = LightDriver;
