def percentage_audio(audio_org, audio_mod):
    percentage = 0
    for i in range(audio_org):
        percentage = (float(audio_org(i)) / float(audio_mod(i))) * 100
    return percentage
