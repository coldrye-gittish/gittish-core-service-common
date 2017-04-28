# TBD:LICENSE


# TBD:DOCUMENT
class ServiceBase:

  def add_to_server(self, server):
    self.add_services(server)


# TBD:DOCUMENT
class ValidatorBase:

  def validate(self, request, context):
    pass


# TBD:DOCUMENT
class ProgrammableValidatorBase(ValidatorBase):

  def validate(self, request, context):
    return self._validator.validate(request, context)

  def set_validator(self, validator):
    self._validator = validator

# vim: expandtab:ts=2:sw=2:
