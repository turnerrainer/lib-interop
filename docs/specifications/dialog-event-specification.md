# Interoperable Dialog Event Specification
**The Open Voice Network**
**Architecture Work Group of the Technical Committee**

|||
|-|-|
|Status|Draft| 
|Version|1.0|
|Date|November 30, 2022|

# Table of Contents 

# Chapter 0 - Scope and Introduction 

## 0.1 Document Scope
This document specifies the format for Open Voice Network (OVON) interoperable dialog events.  The requirements for this specification are given in [Interoperable Dialog Event Requirements](../requirements/ovon-dialog-event-requirements.md).

## 0.2 Purpose of a Dialog Event

Interoperable conversational agents will need to process user inputs that may have been collected by another conversational agent. In order to do this, agents must agree on a format for representing user inputs that all conversational agents that conform to OVON interoperability standards can understand. The purpose of a dialog Event is to define a generic standardized data structure that can be used in any part of a dialog system to express a ‘language event,’ that is to say any information associated with a phrase, utterance or part of an utterance.  These could be user or system events.  Dialog Events span a certain time period and are associated with a single speaker. 

These Events can be used to express whole utterances, phrases or slices of time in a stream. These Events are used to represent user inputs of various types, primarily linguistic inputs such as speech or text, but also potential multimodal inputs, such as selections on a touchscreen. This document will focus on speech and text, while not ruling out multimodal inputs.

Events could be joined together to form streams, for example to represent continuous input or output of a dialog system.

# Representation

This specification defines a logical schema for a dialog event.  Any syntax that can support dictionary key-value pairs and lists could be used (e.g. JSON or YML).  XML is also possible but would require additional specification regarding how key-value pairs and arrays are to be specifically realised.  

# Schema

The structure of a JSON dialog event is defined below as a JSON Schema. As noted above this does not preclude the event being represented in formats other than JSON.

[schema-definition](../../schemas/dialog-event.json "")

