from dataclasses import dataclass

from pydantic import BaseModel, ValidationError


@dataclass
class FormErrors:
    values: dict[str, str] | None = None

    def __getattr__(self, item):
        if self.values:
            return self.values.get(item)
        return None


class BaseForm(BaseModel):
    errors: FormErrors | None = None

    @classmethod
    def validate_form(cls, form) -> "BaseForm":
        fields = {key: value for key, value in form.items()}
        try:
            validated_form = cls(**fields)  # type: ignore
        except ValidationError as e:
            fields["errors"] = FormErrors(
                values={
                    err["loc"][0]: err["msg"].split(maxsplit=2)[2] for err in e.errors()
                }
            )
            return cls.model_construct(**fields)
        return validated_form
