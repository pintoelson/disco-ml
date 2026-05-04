# Discussion #8521: Docs opaque about Datalist
**Repository:** Project-MONAI/MONAI
**Author:** DanielNobbe
**Created At:** 2025-07-25T19:14:57Z

## Description
As a newcomer to MONAI, it is not clear to me what a datalist is, and I feel the documentation and tutorials also do not really explain this. I assume it's a Decathlon datalist, but even their [website](http://medicaldecathlon.com/) does not specify a format.

The background to this is that I'd like to make a datalist file for my own dataset.

If someone could point me to a description of the datalist format, I'll be happy to add it to the documentation and tutorials.

## Comments
### Comment by NabJa at 2025-08-05T08:09:04Z
I assume you mean the [Decathlon datalist ](https://docs.monai.io/en/stable/data.html#decathlon-datalist)? I think its well documented already. For custom datasets I would recommend using one of the [Generic Interfaces](https://docs.monai.io/en/stable/data.html#generic-interfaces).

### Comment by DanielNobbe at 2025-08-05T08:23:32Z
I encountered this while attempting to train the Auto3DSeg AutoRunner pipeline, which requires that custom data is formatted as a datalist. 
And I disagree that it's well-documented under that link: yes, it does mention that there is a list of items with 'image' and 'label' fields, but it does not clarify other things about the format, e.g. that there are a 'train' and 'test' list and that there can be certain metadata fields.

The [`run_with_minimal_input`](https://github.com/Project-MONAI/tutorials/blob/main/auto3dseg/docs/run_with_minimal_input.md) tutorial page specifies it a bit more, and following that one it's possible to get something working with Auto3DSeg. Formatting a datalist with all of the relevant metadata (which is important when running experiments imo), is only possible when studying the format after downloading a MedicalDecathlon dataset. A step that I think should not be necessary to start working with Auto3DSeg.

As I said, I can add this to the documentation, but if I'm really the only one seeing this as an issue I guess it's not needed.
