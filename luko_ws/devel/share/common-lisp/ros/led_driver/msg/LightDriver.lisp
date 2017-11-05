; Auto-generated. Do not edit!


(cl:in-package led_driver-msg)


;//! \htmlinclude LightDriver.msg.html

(cl:defclass <LightDriver> (roslisp-msg-protocol:ros-message)
  ((op
    :reader op
    :initarg :op
    :type cl:string
    :initform "")
   (image
    :reader image
    :initarg :image
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0)))
)

(cl:defclass LightDriver (<LightDriver>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <LightDriver>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'LightDriver)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name led_driver-msg:<LightDriver> is deprecated: use led_driver-msg:LightDriver instead.")))

(cl:ensure-generic-function 'op-val :lambda-list '(m))
(cl:defmethod op-val ((m <LightDriver>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader led_driver-msg:op-val is deprecated.  Use led_driver-msg:op instead.")
  (op m))

(cl:ensure-generic-function 'image-val :lambda-list '(m))
(cl:defmethod image-val ((m <LightDriver>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader led_driver-msg:image-val is deprecated.  Use led_driver-msg:image instead.")
  (image m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <LightDriver>) ostream)
  "Serializes a message object of type '<LightDriver>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'op))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'op))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'image))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) ele) ostream))
   (cl:slot-value msg 'image))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <LightDriver>) istream)
  "Deserializes a message object of type '<LightDriver>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'op) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'op) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'image) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'image)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:aref vals i)) (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<LightDriver>)))
  "Returns string type for a message object of type '<LightDriver>"
  "led_driver/LightDriver")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'LightDriver)))
  "Returns string type for a message object of type 'LightDriver"
  "led_driver/LightDriver")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<LightDriver>)))
  "Returns md5sum for a message object of type '<LightDriver>"
  "94104f9d0ed4c5d119270c5f8f23d22b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'LightDriver)))
  "Returns md5sum for a message object of type 'LightDriver"
  "94104f9d0ed4c5d119270c5f8f23d22b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<LightDriver>)))
  "Returns full string definition for message of type '<LightDriver>"
  (cl:format cl:nil "string op~%uint32[] image~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'LightDriver)))
  "Returns full string definition for message of type 'LightDriver"
  (cl:format cl:nil "string op~%uint32[] image~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <LightDriver>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'op))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'image) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <LightDriver>))
  "Converts a ROS message object to a list"
  (cl:list 'LightDriver
    (cl:cons ':op (op msg))
    (cl:cons ':image (image msg))
))
