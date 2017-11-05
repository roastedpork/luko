;; Auto-generated. Do not edit!


(when (boundp 'mbed_interface::JointAngles)
  (if (not (find-package "MBED_INTERFACE"))
    (make-package "MBED_INTERFACE"))
  (shadow 'JointAngles (find-package "MBED_INTERFACE")))
(unless (find-package "MBED_INTERFACE::JOINTANGLES")
  (make-package "MBED_INTERFACE::JOINTANGLES"))

(in-package "ROS")
;;//! \htmlinclude JointAngles.msg.html


(defclass mbed_interface::JointAngles
  :super ros::object
  :slots (_joints ))

(defmethod mbed_interface::JointAngles
  (:init
   (&key
    ((:joints __joints) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _joints __joints)
   self)
  (:joints
   (&optional __joints)
   (if __joints (setq _joints __joints)) _joints)
  (:serialization-length
   ()
   (+
    ;; float32[] _joints
    (* 4    (length _joints)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32[] _joints
     (write-long (length _joints) s)
     (dotimes (i (length _joints))
       (sys::poke (elt _joints i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32[] _joints
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joints (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joints i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get mbed_interface::JointAngles :md5sum-) "e2a0e438b445b98def0f0ba6a2a85f58")
(setf (get mbed_interface::JointAngles :datatype-) "mbed_interface/JointAngles")
(setf (get mbed_interface::JointAngles :definition-)
      "float32[] joints

")



(provide :mbed_interface/JointAngles "e2a0e438b445b98def0f0ba6a2a85f58")


