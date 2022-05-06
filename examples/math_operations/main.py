import kfp
import kfp.dsl as dsl

from adding import add_op, divmod_op

@dsl.pipeline(
  name='Addition pipeline',
  description='An example pipeline that performs addition calculations.'
)
def add_pipeline(
  a='1',
  b='7',
  c='3'
):
  # Passes a pipeline parameter and a constant value to the `add_op` factory
  # function.
  first_task = add_op(a, 4)
  # Passes an output reference from `first_add_task` and a pipeline parameter
  # to the `add_op` factory function. For operations with a single return
  # value, the output reference can be accessed as `task.output` or
  # `task.outputs['output_name']`.
  second_task = add_op(first_task.output, b)

  third_task = divmod_op(first_task.output, 
                              second_task.output)

  result_task = add_op(third_task.outputs['quotient'], c)

if __name__ == "__main__":
    # execute only if run as a script
    kfp.compiler.Compiler().compile(
        pipeline_func=add_pipeline,
        package_path='add_div_pipeline.yaml')