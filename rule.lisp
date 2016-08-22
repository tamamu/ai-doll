(defmacro let1 (vname val &body body)
  `(let ((,vname ,val))
    ,@body))

(defvar *memory*)

(defun $draw (tar st)
  (let1 it (assoc tar *memory*)
    (if (null it)
      nil
      (assoc st (cdr it)))))

(defun $op (st)
  `(:unknown ,st))

(defun yorn (st)
  (cond ((eq (car st) 'ing?)
         (let* ((A (cadr st))
                (B (caddr st))
                (it ($draw A `(does ,B :now))))
          (if (not (null it))
            it
            `(:unknown ,($op `(A :does B))))))
        (t nil)))
