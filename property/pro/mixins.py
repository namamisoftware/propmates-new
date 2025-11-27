class MediaMixin:
    def get_media_data(self, obj):
        images = []
        video = None

        # 1) Direct related media
        if hasattr(obj, "media") and obj.media.exists():  
            for m in obj.media.all():
                if m.image:
                    images.append(m.image.url)
                if m.image_360:
                    images.append(m.image_360.url)

                if not video and m.video_url:
                    video = m.video_url

                if not video and m.video_file:
                    video = m.video_file.url

        # 2) Reverse lookup
        else:
            for rel in obj._meta.get_fields():
                if rel.one_to_many and rel.auto_created:
                    rel_name = rel.get_accessor_name()
                    qs = getattr(obj, rel_name).all()

                    if qs.exists():
                        for m in qs:
                            if hasattr(m, "image") and m.image:
                                images.append(m.image.url)
                            if hasattr(m, "image_360") and m.image_360:
                                images.append(m.image_360.url)
                            if hasattr(m, "video_url") and m.video_url:
                                video = m.video_url
                            if hasattr(m, "video_file") and m.video_file:
                                video = m.video_file.url
                        break

        return images, video  
